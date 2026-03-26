import psycopg2


# Rellenar datos con los de verdad...

def get_connection():
    return psycopg2.connect(
        dbname="ree_db",
        user="proyectoree",
        password="REE2026",
        host="localhost",
        port="5432"
    )