from pynput import keyboard

class Hotkey(object):
   
    def __init__(self, f1Callback, f2Callback, f3Callback):
        self.COMBINATIONS = [
            {keyboard.Key.f1},
            {keyboard.Key.f2},
            {keyboard.Key.f3}
        ]

        self.current = set()
        self.onF1 = f1Callback
        self.onF2 = f2Callback
        self.onF3 = f3Callback

    def execute(self, value):
        print (f"Detected hotkey={value}")
        if value == keyboard.Key.f1:
            print('f1')
            self.onF1()
        if value == keyboard.Key.f2:
            print('f2')
            self.onF2()
        if value == keyboard.Key.f3:
            print('f3')
            self.onF3()


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

# from pynput import keyboard

# COMBINATIONS = [
#     {keyboard.Key.shift, keyboard.KeyCode(char='a')},
#     {keyboard.Key.shift, keyboard.KeyCode(char='b')}
# ]

# current = set()

# def execute(key=None):
#     print (f"Detected hotkey={key}")

# def on_press(key):
#     if any([key in COMBO for COMBO in COMBINATIONS]):
#         current.add(key)
#         if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
#             execute()

# def on_release(key):
#     if any([key in COMBO for COMBO in COMBINATIONS]):
#         current.remove(key)

# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()