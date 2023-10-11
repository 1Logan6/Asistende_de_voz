import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
from pygame import mixer
import subprocess as sub
import os


#Nombre del bot
name = 'alex'
#Esto para esccuhar
listener = sr.Recognizer()

#Esto es para que la maquina hable
engine = pyttsx3.init()

#Esto para escoger la voz
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)

# #Esto es el saludo del bot
# engine.say("Buenas dias, estimado caballero")
# #Y esto hace que espere antes de otra accion
# engine.runAndWait()

#Diccionario de sitios web
sites = {
    'google':'google.com',
    'youtube':'youtube.com',
    'facebook':'facebook.com',
    'whatsapp':'web.whatsapp.com'
}

#La r es porque da problema la cadena con los diagonales invertidos
programs = {
    'spotify': r"C:\Users\saibo\AppData\Roaming\Spotify\Spotify.exe",
    'discord': r"C:\Users\saibo\AppData\Local\Discord\app-1.0.9018\Discord.exe"
}


def write(f):
    talk("¿Que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("notas.txt", shell=True)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen ():
    try:
        with sr.Microphone() as source:
            print("I can hear you...")
            voice = listener.listen(source)
            #Sin el language habla en ingles el bobo
            rec = listener.recognize_google(voice, language= 'ES')
            rec = rec.lower()
            print(rec)
            if name in rec:
                rec = rec.replace(name, '')
                # print(rec)
    except:
        pass
    
    return rec

# def run():
#     rec = listen()
#     if 'reproduce' in rec:
#         music = rec.replace('reproduce', '')
#         talk("Reproduciendo " + music)
#         pywhatkit.playonyt(music)

def run():
    while True:
        rec = listen()
        
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search,1)
            print(search + ": " + wiki)
            talk(wiki)
        elif 'alarma' in rec:
            num = rec.replace('alarma', '')
            num = num.strip()
            talk("Alarma programada para las " + num + " horas")
            # Obtener la hora actual en el formato HH:MM
            current_time = datetime.datetime.now().strftime('%H:%M')
            # Esperar hasta que la hora actual coincida con la hora de la alarma
            while current_time != num:
                current_time = datetime.datetime.now().strftime('%H:%M')

            print("Buenos dias dormilon!")
            mixer.init()
            mixer.music.load("Mariscones.mp3")
            mixer.music.play()
            
            # Permitir al usuario detener la alarma con la tecla "s"
            while True:
                if keyboard.read_event().name == "s":
                    mixer.music.stop()
                    break
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
            for app in programs:
                if app in rec:
                    talk(f'Abriendo {app}')
                    os.startfile(programs[app])
                    
        elif 'escribe' in rec:
            try:
                with open("notas.txt", 'a') as f:
                    write(f)
            
            except FileNotFoundError as e:
                file = open("notas.txt" , 'w')
                write(file)
        
        elif 'termina' in rec:
            talk('Adios bb!')
            break
            
            
        
if __name__ == '__main__':
    run()