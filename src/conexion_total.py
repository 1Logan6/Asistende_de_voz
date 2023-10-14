import psycopg2

def establecer_conexion():
    conn = psycopg2.connect(
        database="nombre_de_base_de_datos",
        user="tu_usuario",
        password="tu_contraseña",
        host="localhost",
        port="5432"
    )
    return conn

def cerrar_conexion(conn):
    conn.close()
