import speech_recognition as sr #Alias de la libreria
import pyttsx3, pywhatkit, wikipedia,datetime,keyboard
from pygame import mixer


name = "Angel"
listener = sr.Recognizer()#Empieza a reconocer
engine= pyttsx3.init() #iniciacion de la libreria

voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)#Tomamos la voz de la libreria

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone()as source:
            print("Escuchando siuuu")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower() #Tomar testo y convertir a minus
            if name in rec:
                rec = rec.replace(name,'')
    except:
        pass
    return rec

def run_Virtual():
    while True:
        rec=listen()
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo por las ordenes de cr7" + music)
            talk("Reproduce" + music)
            pywhatkit.playonyt(music)
        elif "busca" in rec:
            search = rec.replace('busca','')
            wikipedia.set_lang("es")
            wiki =wikipedia.summary(search, 2)
            print(search + ": " + wiki)
            talk(wiki)
        elif "alarma" in rec:
            num = rec.replace("alarma", '')
            num= num.strip()
            talk("alarma activada a las" + num + " horas")
            while True: 
                if datetime.datetime.now().strftime('%H:%M') == num:
                    print("DESPIERTA!!!")
                    mixer.init()
                    mixer.music.load("Cr7Alarma.mp3")
                    mixer.music.play()
                    if keyboard.read_key() == "s":
                        mixer.music.stop()
                        break
                    #La alarma funciona con un sistema de 24 horas.
         
if __name__ == '__main__':
            run_Virtual()