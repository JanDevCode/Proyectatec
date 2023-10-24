import speech_recognition as sr
import subprocess as sub
import pyttsx3, pywhatkit, wikipedia,datetime,keyboard,colores,os
from pygame import mixer

name = "Angel"
listener = sr.Recognizer()#Empieza a reconocer
engine= pyttsx3.init() #iniciacion de la libreria

voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)#Tomamos la voz de la libreria
engine.setProperty('rate', 145)

sites={
        'google':'google.com',
        'youtube':'youtube.com',
        'facebook':'facebook.com',
        'whatsapp':'web.whatsapp.com',
        'cursos':'platzi.com',
}

# files={
#      'carta':'aqui va el nombre del archivo 1'
#      'cedula':'aqui va el nombre del archivo 2'
#     'foto':'aqui va el nombre del archivo 3'
#    LA FUNCION NO ESTA DISPONIBLE AUN PORQUE EL ARCHIVO DEBE DE ESTAR DENTRO DEL PROYECTO
# }

programs={
    'telegram': r"ubicacion del ejecutable",
    'Spotify': r"ubicacion del ejecutable",
    'Netflis: r"ubicacion del ejecutable",
    'Minecraft': r"ubicacion del ejecutable",
    'discord': r"Ubicacion del arcihvo"
    'Word': r"ubicacion del archivo"
    #La letra r es para indicarle que toda la barra es string.
    #Es importante la terminacion "etse"

}

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    listener = sr.Recognizer()     
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source)
        pc = listener.listen(source)


    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
 
    except sr.UnknownValueError:
        print("No te entendí, intenta otra vez")
        if name in rec:
            rec = rec.replace(name, '')
    return rec

def run_Virtual():
 while True:
        try:
            rec = listen()
        except UnboundLocalError:
            print("No te entendí, intenta de nuevo")
            continue     
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
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
        elif 'colores' in rec:
            talk("Enseguida")
            colores.capturando()
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo{site}')
            for app in programs:
                if app in rec:
                    talk (f'Abriendo {app}')
                    os.startfile(programs[app])        
        # elif 'archivo' in rec:
        #     for file in files:
        #         if file in rec:
        #             sub.Popen([files[file]], shell=True)
        #             sub.Popen abre archivos
        #              Esta funcion no esta probada debido a que los archivos deben
        #             de estar dentro de la carpeta del proyecto pero en el video menciona que
        #             prosimamente lo solucionarà
        #             talk(f'Abriendo {file}')
        elif "redacta" in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write:(f)

            except FileNotFoundError as e:
                file=open("nota.txt", 'w')
                write(file)
        elif 'termina' in rec:
            talk("Adios bichoLover")
            break

def write(f):
    talk("¿Que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesp)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)
if __name__ == '__main__':
            run_Virtual()    