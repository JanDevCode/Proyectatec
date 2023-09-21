import speech_recognition as sr #Alias de la libreria
import pyttsx3, pywhatkit

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
            rec = listener.recognize_google(pc)
            rec = rec.lower() #Tomar testo y convertir a minus
            if name in rec:
                rec = rec.replace(name,'')
    except:
        pass
    return rec

def run_Virtual():
    rec=listen()
    if 'reproduce' in rec:
        music = rec.replace('reproduce', '')
        print("Reproduciendo por las ordenes de cr7" + music)
        talk("Reproduce" + music)
        pywhatkit.playonyt(music)

if __name__ == '__main__':
    run_Virtual()