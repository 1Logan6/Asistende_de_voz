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

label_title=Label(main_window, text="Alex AI", bg=("#E684AE"), fg=("#240b36"),
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
    windows_apps.title("Agrega web")
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
    print(nombre," no ", ruta)

    try:
        print(nombre," si ", ruta)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO webs (nombre_web, ruta_web) VALUES (%s, %s);", (nombre, ruta))
        conn.commit()

    finally:
        conexion_total.cerrar_conexion(conn)
        
def save_bd_app(nombre, ruta):
    conn = conexion_total.establecer_conexion()
    print(nombre," no ", ruta)

    try:
        print(nombre," si ", ruta)
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
    

listado_webs = {}
list_webs(listado_webs)

# def list_webs_window():
#     windows_webs = Toplevel()
#     windows_webs.title("Listas web")
#     windows_webs.configure(bg="#33FFD1")
#     windows_webs.geometry("500x300")
#     windows_webs.resizable(0,0)
#     main_window.eval(f'tk::PlaceWindow {str(windows_webs)} center')
    
#     title_label = Label(windows_webs, text="lista de apps", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
#     title_label.pack(pady=3)
    
    
#     name_label = Label(windows_webs, text="Nombre del sitio web", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
#     name_label.pack(pady=2)
    
#     # name_web_entry = Entry(windows_webs, width=30)
#     # name_web_entry.pack(pady=1)
    
    
#     route_label = Label(windows_webs, text="Ruta del sitio web", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
#     route_label.pack(pady=2)
    
#     # route_web_entry = Entry(windows_webs, width=40)
#     # route_web_entry.pack(pady=1)
    
    
#     # save_button = Button(windows_webs, text="Guardar", bg='#a17fe0', fg="white", width=8, height=2, command=add_webs)
#     # save_button.pack(pady=6)

def list_webs_window():
    windows_webs = Toplevel()
    windows_webs.title("Lista de Sitios Web")
    windows_webs.configure(bg="#33FFD1")
    windows_webs.geometry("500x300")
    windows_webs.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(windows_webs)} center')

    title_label = Label(windows_webs, text="Lista de Sitios Web", fg="white", bg="#33FFD1", font=('Arial', 15, 'bold'))
    title_label.pack(pady=3)

    # # Supongamos que tienes un diccionario con los sitios web
    # sitios_web = {
    #     "Sitio1": "Ruta1",
    #     "Sitio2": "Ruta2",
    #     "Sitio3": "Ruta3",
    # }

    listbox = Listbox(windows_webs)
    listbox.pack(pady=5)

    for nombre, ruta in listado_webs.items():
        listbox.insert(END, nombre)

    def mostrar_ruta_seleccionada(event):
        seleccion = listbox.get(listbox.curselection())
        ruta_label.config(text=f"Ruta del sitio web: {listado_webs[seleccion]}")

    listbox.bind("<<ListboxSelect>>", mostrar_ruta_seleccionada)

    ruta_label = Label(windows_webs, text="Ruta del sitio web:", fg="white", bg="#33FFD1", font=('Arial', 15, 'bold'))
    ruta_label.pack(pady=2)

    windows_webs.mainloop()


def list_apps_window():
    pass

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

        elif "termina" in rec:
            talk("Adios bb!")
            break

button_listen = Button(main_window, text="Escuchar", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=run)
button_listen.pack(pady=10)

button_talk = Button(main_window, text="Hablar", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=read_and_talk)
# button_talk.place(x=620, y=80, width=100, height=30)
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

main_window.mainloop()