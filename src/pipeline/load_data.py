from datetime import datetime
from api.api_client import get_generacion_data
from db.db_client import get_connection

import json


class LoadDataPipeline:

    def load_mock_data(self):
        with open("src/data/mock_data.json") as f:
            return json.load(f)

    def __init__(self):
        self.conn = None
        self.cursor = None

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
                fecha = punto.get("datetime")
                valor = punto.get("value")

                if not fecha or valor is None:
                    continue  # evita datos inválidos

                try:
                    fecha_dt = datetime.fromisoformat(fecha.replace("Z", "+00:00"))

                    self.cursor.execute(
                        """
                        INSERT INTO generacion (fecha, tipo, valor)
                        VALUES (%s, %s, %s)
                        """,
                        (fecha_dt, nombre, valor)
                    )

                except Exception as e:
                    print(f"Error insertando dato: {e}")

    def run(self):
        try:
            print("Obteniendo datos de la API...")
            #data = get_generacion_data(
            #            "2023-01-01T00:00",
            #            "2023-01-01T05:00")
            data = self.load_mock_data()
            

            print("Conectando a la base de datos...")
            self.connect_db()

            print("Insertando datos...")
            self.insert_data(data)

            self.conn.commit()
            print("Datos insertados correctamente")

        except Exception as e:
            print(f"Error en el pipeline: {e}")

        finally:
            self.close_db()


if __name__ == "__main__":
    pipeline = LoadDataPipeline()
    pipeline.run()