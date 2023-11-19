import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
from pygame import mixer
import subprocess as sub
import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import threading as tr
import conexion_total


main_window = Tk()
main_window.title("Alex AI")

main_window.geometry("1200x800")
main_window.resizable(0,0)
main_window.configure(bg='#79CBCA')

comandos= """
    Los comandos que tiene Alex son:
    -Reproduce... (Cancion)
    -Busca...(informacion)
    -Abre...(pagina o app)
    -Alarma...(formato 24h)
    -Escribe...(tomar notas)
    -Termina (cierra el microfono)
"""

canvas_comandos = Canvas(bg="#E100FF", height=300, width=280)
canvas_comandos.place(x=0, y=0)
canvas_comandos.create_text(120,80, text=comandos, fill="white", font='Arial 10')

label_title=Label(main_window, text="Alex", bg=("#79CBCA"), fg=("#240b36"),
                  font=('Arial',30,'bold'))
label_title.pack(pady=10)

text_info = Text(main_window, bg="#E100FF", fg="white")
text_info.place(x=0, y=350, height=450, width=280)

cbum_photo = ImageTk.PhotoImage(Image.open("cbum2.jpg"))
window_photo = Label(main_window, image=cbum_photo)
window_photo.pack(pady=5)


# Nombre del bot
name = "alex"
# Esto para esccuhar
listener = sr.Recognizer()

# Esto es para que la maquina hable
engine = pyttsx3.init()

# Esto para escoger la voz
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 145)

# #Esto es el saludo del bot
# engine.say("Buenas dias, estimado caballero")
# #Y esto hace que espere antes de otra accion
# engine.runAndWait()

def load_webs(sites):
    conn = conexion_total.establecer_conexion()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM webs;")
        resultados = cursor.fetchall()
        for fila in resultados:
            nombre_web, ruta_web = fila
            sites[nombre_web] = ruta_web

    finally:
        conexion_total.cerrar_conexion(conn)

def load_apps(programs):
    conn = conexion_total.establecer_conexion()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM apps;")
        resultados = cursor.fetchall()
        for fila in resultados:
            nombre_app, ruta_app = fila
            programs[nombre_app] = ruta_app

    finally:
        conexion_total.cerrar_conexion(conn)

# Diccionario de sitios web
sites = {}
load_webs(sites)
# La r es porque da problema la cadena con los diagonales invertidos
programs = {}
load_apps(programs)

def write(f):
    talk("¿Que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("notas.txt", shell=True)
    
def read_and_talk():
    text = text_info.get("1.0","end")
    talk(text)
    
def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)

def clock(rec):
    num = rec.replace("alarma", "")
    num = num.strip()
    talk("Alarma programada para las " + num + " horas")
    # Obtener la hora actual en el formato HH:MM
    current_time = datetime.datetime.now().strftime("%H:%M")
    # Esperar hasta que la hora actual coincida con la hora de la alarma
    
    if num[0] != '0' and len(num) <5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print("Buenos dias dormilon!")
            mixer.init()
            mixer.music.load("Mariscones.mp3")
            mixer.music.play()
        else: 
            continue
        if keyboard.read_key() == 's':
            mixer.music.stop()
            break
        
def add_webs_window():
    global name_web_entry, route_web_entry
    
    windows_webs = Toplevel()
    windows_webs.title("Agrega web")
    windows_webs.configure(bg="#33FFD1")
    windows_webs.geometry("500x300")
    windows_webs.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(windows_webs)} center')
    
    title_label = Label(windows_webs, text="Agregar sitio web", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    title_label.pack(pady=3)
    
    
    name_label = Label(windows_webs, text="Nombre del sitio web", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    name_label.pack(pady=2)
    
    name_web_entry = Entry(windows_webs, width=30)
    name_web_entry.pack(pady=1)
    
    
    route_label = Label(windows_webs, text="Ruta del sitio web", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    route_label.pack(pady=2)
    
    route_web_entry = Entry(windows_webs, width=40)
    route_web_entry.pack(pady=1)
    
    
    save_button = Button(windows_webs, text="Guardar", bg='#a17fe0', fg="white", width=8, height=2, command=add_webs)
    save_button.pack(pady=6)

def add_apps_window():
    global name_app_entry, route_app_entry
    
    windows_apps = Toplevel()
    windows_apps.title("Agrega aplicacion")
    windows_apps.configure(bg="#33FFD1")
    windows_apps.geometry("500x300")
    windows_apps.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(windows_apps)} center')
    
    title_label = Label(windows_apps, text="Agregar aplicacion", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    title_label.pack(pady=3)
    
    
    name_label = Label(windows_apps, text="Nombre de la aplicacion", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    name_label.pack(pady=2)
    
    name_app_entry = Entry(windows_apps, width=30)
    name_app_entry.pack(pady=1)
    
    
    route_label = Label(windows_apps, text="Ruta de la aplicacion", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    route_label.pack(pady=2)
    
    route_app_entry = Entry(windows_apps, width=50)
    route_app_entry.pack(pady=1)
    
    
    save_button = Button(windows_apps, text="Guardar", bg='#a17fe0', fg="white", width=8, height=2, command=add_apps)
    save_button.pack(pady=6)
    
def add_webs():
    name_web = name_web_entry.get().strip()
    route_web = route_web_entry.get().strip()
    
    save_bd_web(name_web, route_web)
    sites[name_web] = route_web
    name_web_entry.delete(0, "end")
    route_web_entry.delete(0, "end")

def add_apps():
    name_app = name_app_entry.get().strip()
    route_app = route_app_entry.get().strip()
    
    save_bd_app(name_app,route_app)
    programs[name_app] = route_app
    name_app_entry.delete(0, "end")
    route_app_entry.delete(0, "end")
    
def save_bd_web(nombre, ruta):
    conn = conexion_total.establecer_conexion()

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO webs (nombre_web, ruta_web) VALUES (%s, %s);", (nombre, ruta))
        conn.commit()

    finally:
        conexion_total.cerrar_conexion(conn)
        
def save_bd_app(nombre, ruta):
    conn = conexion_total.establecer_conexion()

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO apps (nombre_app, ruta_app) VALUES (%s, %s);", (nombre, ruta))
        conn.commit()

    finally:
        conexion_total.cerrar_conexion(conn)

def list_webs(listado_webs):
    conn = conexion_total.establecer_conexion()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM webs;")
        resultados = cursor.fetchall()
        for fila in resultados:
            nombre_web, ruta_web = fila
            listado_webs[nombre_web] = ruta_web

    finally:
        conexion_total.cerrar_conexion(conn)
    
def list_apps(listado_apps):
    conn = conexion_total.establecer_conexion()

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM apps;")
        resultados = cursor.fetchall()
        for fila in resultados:
            nombre_app, ruta_app = fila
            listado_apps[nombre_app] = ruta_app

    finally:
        conexion_total.cerrar_conexion(conn)

def edit_webs(seleccion,nueva_ruta):
    conn = conexion_total.establecer_conexion()

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE webs SET ruta_web = %s WHERE nombre_web = %s;", (nueva_ruta,seleccion))
        conn.commit()

    finally:
        conexion_total.cerrar_conexion(conn)

def delete_webs(seleccion):
    conn = conexion_total.establecer_conexion()
    valor_a_eliminar = (seleccion,)

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM webs WHERE nombre_web = %s;", valor_a_eliminar)
        conn.commit()

    finally:
        conexion_total.cerrar_conexion(conn)

def edit_apps(seleccion,nueva_ruta):
    conn = conexion_total.establecer_conexion()

    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE apps SET ruta_app = %s WHERE nombre_app = %s;", (nueva_ruta,seleccion))
        conn.commit()

    finally:
        conexion_total.cerrar_conexion(conn)

def delete_apps(seleccion):
    conn = conexion_total.establecer_conexion()
    valor_a_eliminar = (seleccion,)

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM apps WHERE nombre_app = %s;", valor_a_eliminar)
        conn.commit()

    finally:
        conexion_total.cerrar_conexion(conn)
    
listado_webs = {}
list_webs(listado_webs)

listado_apps = {}
list_apps(listado_apps)

def list_webs_window():
    windows_webs = Toplevel()
    windows_webs.title("Lista de Sitios Web")
    windows_webs.configure(bg="#33FFD1")
    # windows_webs.geometry("500x300")
    windows_webs.geometry("800x500")
    windows_webs.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(windows_webs)} center')

    title_label = Label(windows_webs, text="Lista de Sitios Web", fg="white", bg="#33FFD1", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)

    listbox = Listbox(windows_webs)
    listbox.pack(pady=5)
    
    listado_webs = {}
    list_webs(listado_webs)

    for nombre, ruta in listado_webs.items():
        listbox.insert(END, nombre)

    def mostrar_ruta_seleccionada(event):
        seleccion = listbox.get(listbox.curselection())
        ruta_label.config(text=f"Ruta del sitio web: {listado_webs[seleccion]}")

    listbox.bind("<<ListboxSelect>>", mostrar_ruta_seleccionada)

    ruta_label = Label(windows_webs, text="Ruta del sitio web:", fg="white", bg="#33FFD1", font=('Arial', 15, 'bold'))
    ruta_label.pack(pady=2)
    
     # Botón para editar
    def editar_sitio():
        seleccion = listbox.get(listbox.curselection())
        nueva_ruta = entrada_ruta.get()
        listado_webs[seleccion] = nueva_ruta
        ruta_label.config(text=f"Ruta del sitio web: {nueva_ruta}")
        edit_webs(seleccion,nueva_ruta)
        
        

    boton_editar = Button(windows_webs, text="Editar", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), command=editar_sitio)
    boton_editar.pack(pady=5)

    # Botón para eliminar
    def eliminar_sitio():
        seleccion = listbox.get(listbox.curselection())
        del listado_webs[seleccion]
        listbox.delete(listbox.curselection())
        delete_webs(seleccion)

    boton_eliminar = Button(windows_webs, text="Eliminar", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), command=eliminar_sitio)
    boton_eliminar.pack()

    entrada_ruta = Entry(windows_webs)
    entrada_ruta.pack(pady=5)

    windows_webs.mainloop()

def list_apps_window():
    windows_apps = Toplevel()
    windows_apps.title("Lista de apps")
    windows_apps.configure(bg="#33FFD1")
    # windows_webs.geometry("500x300")
    windows_apps.geometry("800x500")
    windows_apps.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(windows_apps)} center')

    title_label = Label(windows_apps, text="Lista de aplicaciones", fg="white", bg="#33FFD1", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)

    listbox = Listbox(windows_apps)
    listbox.pack(pady=5)
    
    listado_apps = {}
    list_apps(listado_apps)

    for nombre, ruta in listado_apps.items():
        listbox.insert(END, nombre)

    def mostrar_ruta_seleccionada(event):
        seleccion = listbox.get(listbox.curselection())
        ruta_label.config(text=f"Ruta de la app: {listado_apps[seleccion]}",font=('Arial', 10, 'bold'))

    listbox.bind("<<ListboxSelect>>", mostrar_ruta_seleccionada)

    ruta_label = Label(windows_apps, text="Ruta de la app:", fg="white", bg="#33FFD1", font=('Arial', 15, 'bold'))
    ruta_label.pack(pady=2)
    
     # Botón para editar
    def editar_sitio():
        seleccion = listbox.get(listbox.curselection())
        nueva_ruta = entrada_ruta.get()
        listado_apps[seleccion] = nueva_ruta
        ruta_label.config(text=f"Ruta de la app: {nueva_ruta}")
        edit_apps(seleccion,nueva_ruta)
        
        

    boton_editar = Button(windows_apps, text="Editar", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), command=editar_sitio)
    boton_editar.pack(pady=5)

    # Botón para eliminar
    def eliminar_sitio():
        seleccion = listbox.get(listbox.curselection())
        del listado_apps[seleccion]
        listbox.delete(listbox.curselection())
        delete_apps(seleccion)

    boton_eliminar = Button(windows_apps, text="Eliminar", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), command=eliminar_sitio)
    boton_eliminar.pack()

    entrada_ruta = Entry(windows_apps,width=80)
    entrada_ruta.pack(pady=5)

    windows_apps.mainloop()

def add_rutina_window():
    global combo_accion, combo_nombre, combo_dia, entry_hora
    
    windows_rutina = Toplevel()
    windows_rutina.title("Craer rutina")
    windows_rutina.configure(bg="#33FFD1")
    windows_rutina.geometry("700x450")
    windows_rutina.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(windows_rutina)} center')
    
    title_label = Label(windows_rutina, text="Agregar rutina", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    title_label.pack(pady=3)
    
    
    name_label = Label(windows_rutina, text="Que accion quieres que se ejecute?", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    name_label.pack(pady=2)
    
    opciones = ["Abrir", "Reproducir"]
    combo_accion = ttk.Combobox(windows_rutina, values=opciones)
    combo_accion.set("Selecciona una opción")  # Valor por defecto
    combo_accion.pack(pady=1)
    
    # name_web_entry = Entry(windows_rutina, width=30)
    # name_web_entry.pack(pady=1)
    
    
    route_label = Label(windows_rutina, text="Nombre del sitio web/app", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    route_label.pack(pady=2)
    
    
    opciones_apps = list(sites.keys())
    opciones_webs = list(programs.keys())
    opciones = opciones_apps + opciones_webs
    combo_nombre = ttk.Combobox(windows_rutina, values=opciones)
    combo_nombre.set("Selecciona una opción")  # Valor por defecto
    combo_nombre.pack(pady=1)
    
    # route_web_entry = Entry(windows_rutina, width=40)
    # route_web_entry.pack(pady=1)
    
    name_label = Label(windows_rutina, text="Que dia quieres que se ejecute?", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    name_label.pack(pady=2)
    
    opciones = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    combo_dia = ttk.Combobox(windows_rutina, values=opciones)
    combo_dia.set("Selecciona una opción")  # Valor por defecto
    combo_dia.pack(pady=1)
    
    hora_label = Label(windows_rutina, text="Ingresa la hora (formato HH:MM)", fg="white", bg="#33FFD1",
                          font=('Arial', 15, 'bold'))
    hora_label.pack(pady=2)

    entry_hora = ttk.Entry(windows_rutina)
    entry_hora.pack(pady=1)
    
    save_button = Button(windows_rutina, text="Guardar", bg='#a17fe0', fg="white", width=8, height=2, command=add_rutina)
    save_button.pack(pady=6)


def add_rutina():
    accion = combo_accion.get().strip()
    app_web_nombre = combo_nombre.get().strip()
    dia = combo_dia.get().strip()
    hora = entry_hora.get().strip()
    
    print("accion"+accion+" nombre"+app_web_nombre+" dia"+dia+" hora"+hora)
    
    save_bd_rutina(accion, dia, hora, app_web_nombre)
    
    # Limpiar los campos después de crear la rutina
    combo_accion.set("Selecciona una opción")
    combo_nombre.set("Selecciona una opción")
    combo_dia.set("Selecciona una opción")
    entry_hora.delete(0, "end")
    
def save_bd_rutina(accion,dia,hora,app_web_nombre):
    conn = conexion_total.establecer_conexion()

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rutinas (accion, dia, hora, app_web_nombre) VALUES (%s, %s, %s, %s);", (accion,dia,hora,app_web_nombre))
        conn.commit()

    finally:
        conexion_total.cerrar_conexion(conn)

def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    try:
        with sr.Microphone() as source:
            talk("Te escucho chikistrikis")
            voice = listener.listen(source)
            # Sin el language habla en ingles el bobo
            rec = listener.recognize_google(voice, language="ES")
            rec = rec.lower()
            print(rec)
            
            # Esto sirve para corregir el error de detectar álex en lugar de alex.
            if 'álex' in rec:
                rec = rec.replace('álex', "alex")
                
            if name in rec:
                rec = rec.replace(name, "")
                # print(rec)
    except:
        pass

    return rec

def run():
    while True:
        rec = listen()

        if "reproduce" in rec:
            music = rec.replace("reproduce", "")
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
            
        elif "busca" in rec:
            search = rec.replace("busca", "")
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search + ": " + wiki)
            talk(wiki)
            write_text(search + ": " + wiki)
            break
            
        elif "alarma" in rec:
            t = tr.Thread(target=clock, args=(rec,))
            t.start()
                
        elif "abre" in rec:    
            task = rec.replace('abre','').strip()
            if task in sites:
                for task in sites:
                    if task in rec:
                        sub.call(f"start chrome.exe {sites[task]}", shell=True)
                        talk(f"Abriendo {task}")
            elif task in programs:
                for task in programs:
                    if task in rec:
                        talk(f"Abriendo {task}")
                        os.startfile(programs[task])
            else:
                talk(f"No se encontro {task} en ninguna parte, puedes agregarlo con los botones de la derecha")

        elif "escribe" in rec:
            try:
                with open("notas.txt", "a") as f:
                    write(f)

            except FileNotFoundError as e:
                file = open("notas.txt", "w")
                write(file)
                
        elif "rutina" in rec:
            talk(f"Abriendo tas en rutina")

        elif "termina" in rec:
            talk("Adios bb!")
            break

button_listen = Button(main_window, text="Escuchar", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=run)
button_listen.pack(pady=10)

button_talk = Button(main_window, text="Hablar", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=read_and_talk)
button_talk.pack(pady=11)

button_add_webs = Button(main_window, text="Agregar paginas", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=add_webs_window)
button_add_webs.place(x=1000, y=80, width=190, height=40)

button_add_apps = Button(main_window, text="Agregar aplicaciones", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=add_apps_window)
button_add_apps.place(x=1000, y=150, width=190, height=40)

button_list_apps = Button(main_window, text="Listar aplicaciones", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=list_apps_window)
button_list_apps.place(x=1000, y=220, width=190, height=40)

button_list_webs = Button(main_window, text="Listar sitios web", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=list_webs_window)
button_list_webs.place(x=1000, y=290, width=190, height=40)

button_add_webs = Button(main_window, text="Agregar rutina", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=add_rutina_window)
button_add_webs.place(x=1000, y=360, width=190, height=40)

main_window.mainloop()