# Proyecto REE – Pipeline de Datos

## 📦 Requisitos

Antes de empezar, asegúrate de tener instalado:

* Python 3.x
* PostgreSQL
* pip

---

## 🧱 1. Crear la base de datos

Ejecuta el siguiente comando:

```
sudo -u postgres psql -f sql/init.sql
```

Esto creará:

* Base de datos: `ree_db`
* Usuario: `proyectoree`
* Contraseña: `REE2026`
* Tabla: `generacion`

---

## 🔌 2. Configurar conexión a la base de datos

Abre el archivo:

```
src/db/db_client.py
```

Y asegúrate de que la conexión tiene estos valores:

```python
return psycopg2.connect(
    dbname="ree_db",
    user="proyectoree",
    password="REE2026",
    host="localhost",
    port="5432"
)
```

⚠️ IMPORTANTE:
Estos datos deben coincidir con los creados en el script SQL.

---

## 📥 3. Instalar dependencias

Ejecuta:

```
pip install requests psycopg2-binary
```

---

## 🚀 4. Ejecutar el pipeline

Desde la raíz del proyecto:

```
PYTHONPATH=src python src/pipeline/load_data.py
```

---

## ✅ 5. Verificar datos en la base de datos

Conéctate a PostgreSQL:

```
psql -U proyectoree -d ree_db -h localhost
```

Consulta los datos:

```
SELECT * FROM generacion;
```

---

## ⚠️ Notas

* El proyecto actualmente usa datos simulados (mock.json)
* Cambiar en el def run de load_data.py la procedencia de la recogida de datos.
* La API de REE puede ser inestable (no me dejaba conectarme a ella por eso he tenido que simular con mock)
* Ejecutar el script varias veces puede generar duplicados si no se controla

---