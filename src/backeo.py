import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
from pygame import mixer


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
            while True:
                if datetime.datetime.now().strftime('%H:%M') == num:
                    print("Buenos dias dormilon!")
                    mixer.init()
                    mixer.music.load("Mariscones.mp3")
                    mixer.music.play()
                    if keyboard.read_key == "s":
                        mixer.music.stop()
                        break
            
        
if __name__ == '__main__':
    run()