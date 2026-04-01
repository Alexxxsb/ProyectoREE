from datetime import datetime
from api.api_client import get_generacion_data
from db.db_client import get_connection

import logging
import json

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ])

class LoadDataPipeline:

    def load_mock_data(self):
        with open("src/data/mock_data.json") as f:
            return json.load(f)

    def __init__(self):
        self.conn = None
        self.cursor = None

        # Metricas
        self.total = 0;
        self.insertados = 0;    
        self.ignorados = 0;
        self.errores = 0;

    def connect_db(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def close_db(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def insert_data(self, data):
        for tipo in data.get("included", []):
            nombre = tipo.get("type")
    
            for punto in tipo.get("attributes", {}).get("values", []):
                self.total += 1
                fecha = punto.get("datetime")
                valor = punto.get("value")
    
                if not self.validate_data(fecha, valor, nombre):
                    logging.warning(f"Registro inválido: fecha={fecha}, valor={valor}, nombre={nombre}")
                    self.ignorados += 1
                    continue
    
                try:
                    try:
                        fecha_dt = datetime.fromisoformat(fecha.replace("Z", "+00:00"))
                    except Exception:
                        logging.warning(f"Fecha no parseable: {fecha}, omitiendo registro")
                        self.ignorados += 1
                        continue
    
                    # 🔹 1. Insertar tipo si no existe
                    self.cursor.execute(
                        """
                        INSERT INTO tipos_generacion (nombre)
                        VALUES (%s)
                        ON CONFLICT (nombre) DO NOTHING
                        """,
                        (nombre,)
                    )
    
                    # 🔹 2. Obtener ID del tipo
                    self.cursor.execute(
                        """
                        SELECT id FROM tipos_generacion WHERE nombre = %s
                        """,
                        (nombre,)
                    )
                    tipo_id = self.cursor.fetchone()[0]
    
                    # 🔹 3. Insertar en generacion (UPSERT real)
                    self.cursor.execute(
                        """
                        INSERT INTO generacion (fecha, tipo_id, valor)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (fecha, tipo_id)
                        DO UPDATE SET valor = EXCLUDED.valor
                        WHERE generacion.valor IS DISTINCT FROM EXCLUDED.valor
                        """,
                        (fecha_dt, tipo_id, valor)
                    )

                    self.insertados += 1
    
                except Exception as e:
                    logging.error(f"Error insertando dato: {e}")
                    self.errores += 1

    def run(self):
        try:
            logging.info("Obteniendo datos de la API...")
            data = get_generacion_data(
                        "2023-01-01T00:00",
                        "2023-01-01T02:00")
            
            if data is None:
                logging.warning("No se obtuvieron datos de la API, cargando datos mock...")                
                data = self.load_mock_data()
            

            logging.info("Conectando a la base de datos...")
            self.connect_db()

            logging.info("Insertando datos...")
            self.insert_data(data)

            self.conn.commit()
            logging.info("Datos insertados correctamente")

        except Exception as e:
            logging.error(f"Error en el pipeline: {e}")

        finally:
            logging.info("METRICAS DEL PIPELINE")
            logging.info(f"Total registros procesados: {self.total}")
            logging.info(f"Registros insertados: {self.insertados}")
            logging.info(f"Registros ignorados: {self.ignorados}")
            logging.info(f"Registros con errores: {self.errores}")
            self.close_db()
    def validate_data(self, fecha, valor, nombre):
        if not fecha: 
            logging.warning("Fecha no válida, omitiendo registro")
            return False
        if valor is None:
            logging.warning("Valor no válido, omitiendo registro")
            return False
        if not isinstance(valor, (int, float)):
            logging.warning("Valor no numérico, omitiendo registro")
            return False
        if valor < 0:
            logging.warning("Valor negativo, omitiendo registro")
            return False
        if not nombre or not isinstance(nombre, str):
            logging.warning("Nombre de tipo no válido, omitiendo registro")
            return False
        return True

if __name__ == "__main__":
    pipeline = LoadDataPipeline()
    pipeline.run()