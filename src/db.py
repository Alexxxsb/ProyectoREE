import psycopg2


# Rellenar datos con los de verdad...

def get_connection():
    return psycopg2.connect(
        dbname="ree",
        user="postgres",
        password="tu_password",
        host="localhost",
        port="5432"
    )