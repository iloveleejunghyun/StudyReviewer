from pynput import keyboard

class Hotkey(object):
   
    def __init__(self, f2Callback, f3Callback, f4Callback):
        self.COMBINATIONS = [
            {keyboard.Key.f2},
            {keyboard.Key.f3},
            {keyboard.Key.f4}
        ]

        self.current = set()
        self.onF2 = f2Callback
        self.onF3 = f3Callback
        self.onF4 = f4Callback

    def execute(self, value):
        print (f"Detected hotkey={value}")
        if value == keyboard.Key.f2:
            print('f2')
            self.onF2()
        if value == keyboard.Key.f3:
            print('f3')
            self.onF3()
        if value == keyboard.Key.f4:
            print('f4')
            self.onF4()


    def on_press(self, key):
        if any([key in COMBO for COMBO in self.COMBINATIONS]):
            self.current.add(key)
            if any(all(k in self.current for k in COMBO) for COMBO in self.COMBINATIONS):
                self.execute(key)

    def on_release(self, key):
        if any([key in COMBO for COMBO in self.COMBINATIONS]):
            self.current.remove(key)

    def listenDaemon(self):
        import threading
        t = threading.Thread(target=self.listen)
        t.start()
        # with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
        #     listener.join()
    def listen(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
