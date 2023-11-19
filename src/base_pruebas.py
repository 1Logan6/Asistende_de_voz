import psycopg2

def check_database_existence():
    try:
        connection = psycopg2.connect(
            host = 'localhost',
            user = 'Logan',
            password = '16Dicdoky',
            database = 'nueva_prueba',
            port = '5432'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'nombre_de_tabla';")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    except psycopg2.Error as e:
        return False

def create_database_and_tables():
    try:
        connection = psycopg2.connect(
            host = 'localhost',
            user = 'Logan',
            password = '16Dicdoky',
            database = 'postgres',
            port = '5432'
        )
        cursor = connection.cursor()
        # Aquí ejecuta las sentencias SQL para crear la base de datos y las tablas
        cursor.execute("""
                       CREATE DATABASE pruebita
                        WITH
                        OWNER = postgres
                        ENCODING = 'UTF8'
                        CONNECTION LIMIT = -1
                        IS_TEMPLATE = False;
                       """)
        cursor.execute("""CREATE TABLE tablita 
                        (
                        nombre VARCHAR(255),
                        codigo INT);""")
        # Asegúrate de hacer un commit para que los cambios se apliquen.
        connection.commit()
        cursor.close()
        connection.close()
    except psycopg2.Error as e:
        print(f"Error al crear la base de datos: {e}")

# Llama a la función para crear la base de datos y las tablas si no existen.
if not check_database_existence():
    print("La tabla no existe")
    create_database_and_tables()
    print("La tabla creada")



