import playsound
import threading

def ding():
    t = threading.Thread(target=lambda :playsound.playsound('sound/ding.mp3'))
    t.start()
    