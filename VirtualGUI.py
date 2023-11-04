import speech_recognition as sr
import subprocess as sub
import pyttsx3, pywhatkit, wikipedia,datetime,keyboard,colores,os
from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer
import threading as tr
import whatsApp as whapp
import browser
import database
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


#inicio de la ventana
main_window = Tk()
#Testo de la parte de arriba de la ventana
main_window.title("VirtualIA")

#personalizacion
main_window.geometry("1500x900")
main_window.resizable(0,0)
main_window.configure(bg='#1d3557')

comandos = """"
    Comandos que estan disponibles:
    1.- Reproduce...(cancion)
    2.-Busca...(Algo que quieras buscar)
    3.-Abre...(pagina web o app)
    4.-Alarma...(En formato de 24H)
    5.-Archivo...(Nombre del archivo)
    6.-Colores...(Rojo,Azul,Amarillo)
    7.- Termina
"""

label_title = Label(main_window, text="Virtual IA",bg="#ffb703", fg="#f1faee", font=('Arial',20, 'bold'))
label_title.pack(pady=10)

canvas_comandos = Canvas(bg="#f1faee", height=270, width=350)
canvas_comandos.place(x=20, y=80)
canvas_comandos.create_text(175,120, text=comandos, fill="black", font='Arial 11')

text_info = Text(main_window, bg= "#f1faee", fg="black")
text_info.place(x=20,  y=400, height= 270, width=350)

#La ruta puede cambiar dependiendo de la pc en la que se ejecute el programa.
Virtual_photo = ImageTk.PhotoImage(Image.open("C:\\Users\\janco\\Documents\\Proyectatec\\photos\\python.jpg"))
window_photo = Label(main_window, image= Virtual_photo)
window_photo.pack(pady=5)

def mexican_voice():
    change_voice(0)
def spanish_voice():
    change_voice(2)
def english_voice():
    change_voice(1)
def change_voice(id):
    engine.setProperty("voice",voices[id].id)#Tomamos la voz de la libreria
    engine.setProperty('rate', 145)#velocidad de la voz
    talk("Asi se escucha la voz del asistente virtual dependiendo el idioma seleccionado creado por tony, guetze, angel y Jan")

name = "Virtual"
listener = sr.Recognizer()#Empieza a reconocer
engine= pyttsx3.init() #iniciacion de la libreria

voices = engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)#Tomamos la voz de la libreria
engine.setProperty('rate', 145)#velocidad de la voz

def charge_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key, val) = line.split(",")
                val= val.rstrip("\n")
                name_dict[ key]=val
    except FileNotFoundError as e:
        pass


sites= dict()
charge_data(sites, "pages.txt")

files= dict()
charge_data(files, "archivos.txt")

programs= dict()
charge_data(programs, "apps.txt")

contacts = dict()
charge_data(contacts, "contacts.txt")

def talk(text):
    engine.say(text)
    engine.runAndWait()

def read_and_talk():
    text=text_info.get("1.0", "end")
    talk(text)

def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)

def listen():
    listener = sr.Recognizer()  # Crea una instancia de la clase Recognizer
    #rec=""
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        talk("Procedere a escucharte desde este momento.")
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:  # Corrige el nombre de la excepción
        print("No entendi, intenta de nuevo")
    except sr.RequestError as e:
        print("El servicio de Google Speech Recognition service no fue capaz de reconocer el sonido; {0}".format(e))
    return rec
    
#Funciones asociadas a las palabras claves

def reproduce(rec):
    music = rec.replace('reproduce', '')
    print("Reproduciendo " + music)
    talk("Reproduciendo " + music)
    pywhatkit.playonyt(music)

def busca(rec):
    search = rec.replace('busca','')
    wikipedia.set_lang("es")
    wiki =wikipedia.summary(search, 2)
    talk(wiki)
    write_text(search + ": " + wiki)

def thread_alarma(rec):
    t= tr.Thread(target=clock, args=(rec,))
    t.start()
def colores(rec):
    talk("Enseguida")
    colores.capturando()
def abre(rec):
    task = rec.replace('abre', '').strip()

    if task in sites:
                for task in sites:
                    if task in rec:
                        sub.call(f'start chrome.exe {sites[task]}', shell=True)
                        talk(f'Abriendo{task}')
                    elif task in programs:
                         for task in programs:
                             if task in rec:
                                 talk (f'Abriendo {task}')
                                 sub.Popen(programs[task])
                    else:
                        talk("Lo siento parece que aun no has agregado esa app o pagina, usa los botones de agregar")
def archivo(rec):
    file = rec.replace('archivo', '').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
        talk("Lo siento parece que aun no has agregado ese archivo")
def escribe(rec):
    try:
        with open("nota.txt", 'a') as f:
            write(f)
    except FileNotFoundError as e:
        file = open("nota.txt", 'w')
        write(file)
    if 'termina' in rec:
        talk("Adios")
    elif 'termina' in rec:
        talk('adios!')


def clock(rec):
    num= rec.replace('alarma','')
    num= num.strip()
    talk("Alarma activada a las " + num + " horas")
    if num[0] != '0' and len(num) < 5:
        num='0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print("DESPIERTA!!!")
            mixer.init()
            mixer.music.load("Cr7Alarma.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s":
            mixer.music.stop()
            break

def enviar_mensaje(rec):
    talk("A quien quieres enviar el mensaje?")
    contact= listen()
    contact= contact.strip()

    if contact in contacts:
        for cont in contacts:
            if cont == contact:
                contact = contacts[cont]
                talk("¿Que mensaje quieres enviaarle?")
                message = listen()
                talk("Enviando mensaje...")
                whapp.send_menssage(contact, message)
    else:
        talk("parece que aun no has agregado a ese contacto, usa el boton de agregar!")

key_words = {
        'reproduce': reproduce,
        'busca': busca,
        'alarma': thread_alarma,
        'colores': colores,
        'abre': abre,
        'archivo': archivo,
        'escribe': escribe,
        'mensaje': enviar_mensaje
}



def run_Virtual():
    while True:  
        try:     
            rec = listen()
        except UnboundLocalError:
            talk("No entendi, intenta de nuevo")
            continue         
        if 'busca' in rec:
            key_words['busca'](rec)
            break
        else:
            for word in key_words:
                if word in rec:
                    key_words[word](rec)
        if 'Termina' in rec:
            talk("Que tengas un gran dia. Hasta luego")
            break

    main_window.update()

def write(f):
    talk("¿Que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesp)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)

def open_w_files():
    global namefile_entry, pathf_entry
    window_files= Toplevel()
    window_files.title("Agregar archivos")
    window_files.configure(bg="Black")
    window_files.geometry("600x400")
    window_files.resizable(0,0)
    main_window.eval(f"tk::PlaceWindow {str(window_files)} center")

    title_label = Label(window_files, text="Agrega un archivo", fg="white", bg="#434343", font=('Arial',15, 'bold'))
    title_label.pack(pady=6)
    name_label= Label (window_files, text="Nombre del archivo", fg="white", bg="#434343", font=('Arial',10, 'bold')) 
    name_label.pack(pady=3)

    namefile_entry = Entry(window_files)
    namefile_entry.pack(pady=1)

    path_label= Label (window_files, text="Ruta del archivo", bg="white", fg="#434343", font=('Arial',10, 'bold')) 
    path_label.pack(pady=2)

    pathf_entry = Entry(window_files, width=35)
    pathf_entry.pack(pady=1)

    save_button = Button(window_files, text="Guardar", bg='#16222A', fg="white", width=8, height=1, command=add_files)
    save_button.pack(pady=4)

def open_w_apps():

    global nameapps_entry, patha_entry
    window_apps= Toplevel()
    window_apps.title("Agregar apps")
    window_apps.configure(bg="Black")
    window_apps.geometry("600x400")
    window_apps.resizable(0,0)
    main_window.eval(f"tk::PlaceWindow {str(window_apps)} center")

    title_label = Label(window_apps, text="Agrega una app", fg="white", bg="#434343", font=('Arial',15, 'bold'))
    title_label.pack(pady=6)
    name_label= Label (window_apps, text="Nombre de la app", fg="white", bg="#434343", font=('Arial',10, 'bold')) 
    name_label.pack(pady=3)

    nameapps_entry = Entry(window_apps)
    nameapps_entry.pack(pady=1)

    path_label= Label (window_apps, text="Ruta de la app", bg="white", fg="#434343", font=('Arial',10, 'bold')) 
    path_label.pack(pady=2)

    patha_entry = Entry(window_apps, width=35)
    patha_entry.pack(pady=1)

    save_button = Button(window_apps, text="Guardar", bg='#16222A', fg="white", width=8, height=1, command=add_apps)
    save_button.pack(pady=4)

def open_w_pages():
    global namepages_entry, pathp_entry
    window_pages= Toplevel()
    window_pages.title("Agregar paginas web")
    window_pages.configure(bg="Black")
    window_pages.geometry("600x400")
    window_pages.resizable(0,0)
    main_window.eval(f"tk::PlaceWindow {str(window_pages)} center")

    title_label = Label(window_pages, text="Agrega una pagina web", fg="white", bg="#434343", font=('Arial',15, 'bold'))
    title_label.pack(pady=6)
    name_label= Label (window_pages, text="Nombre de la pagina web", fg="white", bg="#434343", font=('Arial',10, 'bold')) 
    name_label.pack(pady=3)

    namepages_entry = Entry(window_pages)
    namepages_entry.pack(pady=1)

    path_label= Label (window_pages, text="URL de la pagina web", bg="white", fg="#434343", font=('Arial',10, 'bold')) 
    path_label.pack(pady=2)

    pathp_entry = Entry(window_pages, width=35)
    pathp_entry.pack(pady=1)

    save_button = Button(window_pages, text="Guardar", bg='#16222A', fg="white", width=8, height=1 , command=add_pages)
    save_button.pack(pady=4)   



def add_files():
    name_file=namefile_entry.get().strip()
    path_file = pathf_entry.get().strip()

    files[name_file] = path_file
    save_data(name_file, path_file, "archivos.txt")
    namefile_entry.delete(0, "end")
    pathf_entry.delete(0, "end")

def add_apps():
    name_file=nameapps_entry.get().strip()
    path_file = patha_entry.get().strip()

    programs[name_file] = path_file
    save_data(name_file, path_file, "apps.txt")
    nameapps_entry.delete(0, "end")
    patha_entry.delete(0, "end")

def add_pages():
    name_page =namepages_entry.get().strip()
    url_pages = pathp_entry.get().strip()

    sites[name_page] = url_pages
    save_data(name_page, url_pages, "pages.txt")
    namepages_entry.delete(0, "end")
    pathp_entry.delete(0, "end") 

def add_contacs():
    name_contact = namecontact_entry.get().strip()
    phone = phone_entry.get().strip()

    contacts[name_contact] = phone
    save_data(name_contact, phone, "contacts.txt")
    namecontact_entry.delete(0, "end")
    phone_entry.delete(0, "end")

def open_w_contacts():
    global namecontact_entry, phone_entry
    window_contacts = Toplevel()
    window_contacts.title("Agrega un contacto")
    window_contacts.configure(bg="#434343")
    window_contacts.geometry("600x400")
    window_contacts.resizable(0,0)
    main_window.eval(f"tk::PlaceWindow {str(window_contacts)} center")


    name_label= Label(window_contacts, text="Nombre del contacto", fg="white", bg="#434343", font=('Arial', 15, 'bold'))
    name_label.pack(pady=2)

    namecontact_entry= Entry(window_contacts)
    namecontact_entry.pack(pady=1)

    phone_label = Label(window_contacts, text="Numero de celular (con codigo del pais)", fg="white", bg="#434343", font=('Arial', 10,'bold'))
    phone_label.pack(pady=2)

    phone_entry = Entry(window_contacts, width=35)
    phone_entry.pack(pady=1)

    save_button = Button(window_contacts, text="Guardar", bg='#FFFFFF', fg="black", width=8, height=1, command=add_contacs) 
    save_button.pack(pady=4)

def save_data(key, value, file_name):
    try:
        with open(file_name, 'a') as f:
            f.write(key + "," + value + "\n")
    except FileNotFoundError as f:
        file = open(file_name, 'a')
        file.write = open(file_name, 'a')

def talk_pages():
    if bool(sites) == True:
        talk("Has agregado las siguientes paginas web")
        for site in sites:
            talk(site)
    else:
        talk("Aun no has agregado paginas web")
def talk_apps():
    if bool(programs) == True:
        talk("Has agregado la siguiente aplicacion")
        for app in programs:
            talk(app)
    else:
        talk("Aun no has agregado una aplicacion")
def talk_files():
    if bool(files) == True:
        talk("Has agregado los siguientes archivos")
        for file in files:
            talk(file)
    else:
        talk("Aun no has agregado archivos")

def talk_contacs():
    if bool(contacts)==True:
        talk("Has agregado los siguientes contactos")
        for cont in contacts:
            talk(cont)
    else:
        talk("Aun no has agregado contactos!")
def give_me_name():
    talk("Hola ¿como te llamas amiguito?")
    name=listen()
    name = name.strip()
    talk(f"Bienvenido {name}")

    try:
        with open("name.txt", 'w') as f:
            f.write(name)
    except FileNotFoundError:
        file = open("name.txt", 'w')
        file.write(name)

def say_hello():
    
        if os.path.exists("name.txt"):
            with open("name.txt") as f:
                for name in f:
                    talk(f"hola, bienvenido {name}")
        else:
            give_me_name()

def thread_hello():
    t=tr.Thread(target=say_hello)
    t.start()

thread_hello()


#Botones
button_voice_mx = Button(main_window, text="Voz de México", fg='#21502D', bg="#FFFFFF", font=("Space mono", 12, "bold"), command=mexican_voice)

button_voice_es = Button(main_window, text="Voz de España", fg='#9B0F0F', bg="#FFFFFF", font=("Space mono", 12, "bold"), command=spanish_voice)

button_voice_us = Button(main_window, text="Voz de EEUU", fg='#0008FF', bg="#FFFFFF", font=("Space mono", 12, "bold"), command=english_voice)

button_listen = Button(main_window, text="Escuchar", fg='#EAEAEA', bg="#000000", font=("Space mono", 14, "bold"), width=10, height=10 ,command=run_Virtual)

button_add_files = Button(main_window, text="Agregar archivos", fg='black', bg="#FFFFFF", font=("Space mono", 12, "bold"), command=open_w_files)

button_add_apps = Button(main_window, text="Agregar apps", fg='black', bg="#FFFFFF", font=("Space mono", 12, "bold"), command=open_w_apps)

button_add_pages = Button(main_window, text="Agregar paginas", fg='black', bg="#FFFFFF", font=("Space mono", 12, "bold"),command=open_w_pages)

button_Speak = Button(main_window, text="Hablar", fg ="white", bg= "black", font=("Space mono", 12,"bold" ), command=read_and_talk)

button_tell_pages = Button(main_window, text="Paginas agregadas", fg='black', bg="#FFFFFF", font=("Space mono", 12, "bold"),command=talk_pages)

button_tell_apps = Button(main_window, text="Apps agregadas", fg='black', bg="#FFFFFF", font=("Space mono", 12, "bold"),command=talk_apps)

button_tell_files = Button(main_window, text="Archivos agregados", fg='black', bg="#FFFFFF", font=("Space mono", 12, "bold"),command=talk_files)

button_add_contacs = Button(main_window, text="Agregar contactos", fg='black', bg="#FFFFFF", font=("Space mono", 12, "bold"),command=open_w_contacts)

button_contactos_agregados = Button(main_window, text="Contactos agregados", fg='black', bg="#FFFFFF", font=("Space mono", 12, "bold"),command=talk_contacs)

#posicionamiento de cada boton
button_voice_mx.place(x=1200, y=73, width=200, height=50)
button_voice_es.place(x=1200, y=156, width=200, height=50)
button_voice_us.place(x=1200, y=240, width=200, height=50)
button_listen.pack(side= BOTTOM, pady=10)
button_Speak.place(x=1200, y=320, width=200, height=50)
button_add_files.place(x=1200, y=360, width=200, height=50)
button_add_apps.place(x=1200, y=420, width=200, height=50)
button_add_pages.place(x=1200, y=500, width=200, height=50)
button_tell_pages.place(x=1180, y=600, width=250, height=50)
button_tell_apps.place(x=1180, y=700, width=250, height=50)
button_tell_files.place(x=1180, y=760, width=250, height=50)
button_add_contacs.place(x=900, y=800, width=250, height=50)
button_contactos_agregados.place(x=400, y=800, width=250, height=50)

main_window.mainloop()