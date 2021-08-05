import platform

import pyttsx3
import speech_recognition as sr

import mimic


class Speaker:

    def __init__(self):
        if platform.system() == 'Linux':
            self.engine = mimic.Mimic()
        else:
            self.engine = pyttsx3.init()
            voice = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voice[0].id)
            # engine.setProperty('rate', 190)
    
    def say(self, args):
        for string in args:
            self.engine.say(string)
        self.engine.runAndWait()


class Listener:

    def listen():
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                audio = r.listen(source)
            
                print("Pasring...")
                text = r.recognize_google(audio, language='es-AR')
                print(text)
        except Exception as e:
            print(e)