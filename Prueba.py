import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("Háblame...")
    audio = recognizer.listen(source)

try:
    text = recognizer.recognize_google(audio, language="es-ES")
    print("Has dicho: " + text)
except sr.UnknownValueError:
    print("No se entendió lo que dijiste")
except sr.RequestError as e:
    print("Error en la solicitud: {0}".format(e))
