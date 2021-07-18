from speak import *

def greetings():
    speak("Welcome back sir")

if __name__ == "__main__":
    greetings()

    while True:
        cmd = listen()