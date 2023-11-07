import psycopg2

def establecer_conexion():
    conn = psycopg2.connect(
        host = 'localhost',
        user = 'Logan',
        password = '16Dicdoky',
        database = 'nueva_prueba',
        port = '5432'
    )
    return conn

def cerrar_conexion(conn):
    conn.close()
