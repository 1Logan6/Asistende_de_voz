import psycopg2
import os

try:
    connection = psycopg2.connect(
        host = 'localhost',
        user = 'Logan',
        password = '16Dicdoky',
        database = 'nueva_prueba',
        port = '5432'
    )
    print("Conexion de pelos")
except Exception as ex:
    print(ex)
    
cursor = connection.cursor()

cursor.execute("SELECT * FROM apps;")
resultados = cursor.fetchall()

# for fila in resultados:
#     print(fila)

# Inicializa un diccionario vacío
datos_apps = {}

# Itera a través de los resultados y construye el diccionario
for fila in resultados:
    nombre_app, ruta_app = fila
    datos_apps[nombre_app] = ruta_app

cursor.close()
connection.close()

# El diccionario datos_apps ahora contiene la información deseada
print(datos_apps)

os.startfile(datos_apps["discord"])

print(datos_apps["spotify"])