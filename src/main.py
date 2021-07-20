from speak import *

out_world = MouthAndEars()

def greetings():
    out_world.speak("""
    Welcome sir, this is jarvis at your service.
    What can I do to help you?
    """)

def back_online():
    out_world.speak("""
    Welcome back sir.
    What can I do to help you?
    """)

if __name__ == "__main__":
    greetings()

    while True:
        cmd = out_world.listen()