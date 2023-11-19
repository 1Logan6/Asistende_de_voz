from datetime import datetime

# Obtener la fecha y hora actual
fecha_y_hora_actual = datetime.now()

# Obtener el día de la semana (0 = lunes, 1 = martes, ..., 6 = domingo)
dia_de_la_semana = fecha_y_hora_actual.weekday()

# Convertir el número del día de la semana a un nombre
nombres_dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
nombre_del_dia = nombres_dias[dia_de_la_semana]

# Imprimir el resultado
print("Hoy es:", nombre_del_dia)