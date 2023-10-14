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

# Diccionario de sitios web
sites = {}

# La r es porque da problema la cadena con los diagonales invertidos
programs = {}


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
        
def add_webs():
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
    
    
    save_button = Button(windows_webs, text="Guardar", bg='#a17fe0', fg="white", width=8, height=2)
    save_button.pack(pady=6)

def add_apps():
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
    
    name_web_entry = Entry(windows_apps, width=30)
    name_web_entry.pack(pady=1)
    
    
    route_label = Label(windows_apps, text="Ruta de la aplicacion", fg="white", bg="#33FFD1", font=('Arial',15,'bold'))
    route_label.pack(pady=2)
    
    route_web_entry = Entry(windows_apps, width=50)
    route_web_entry.pack(pady=1)
    
    
    save_button = Button(windows_apps, text="Guardar", bg='#a17fe0', fg="white", width=8, height=2)
    save_button.pack(pady=6)

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
            for site in sites:
                if site in rec:
                    sub.call(f"start chrome.exe {sites[site]}", shell=True)
                    talk(f"Abriendo {site}")
            for app in programs:
                if app in rec:
                    talk(f"Abriendo {app}")
                    os.startfile(programs[app])

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
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=add_webs)
button_add_webs.place(x=1000, y=80, width=190, height=40)

button_add_apps = Button(main_window, text="Agregar aplicaciones", fg="white", bg="#a17fe0",
                       font=("Arial", 10, "bold"), width = 30, height= 5,  command=add_apps)
button_add_apps.place(x=1000, y=150, width=190, height=40)

main_window.mainloop()