import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[0].id)
# engine.setProperty('rate', 190)

def speak(words):
    engine.say(words)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Pasring...")
        text = r.recognize_google(audio, language='es-AR')
        print(text)
    except Exception as e:
        print(e)
        speak('Please, say it again')