from pynput import mouse, keyboard
import json

class InputCapture:
    def __init__(self, network):
        self.network = network

    def send(self, data):
        self.network.send(json.dumps(data).encode())

    # --- SOURIS ---
    def on_move(self, x, y):
        self.send({"type": "mouse_move", "x": x, "y": y})

    def on_click(self, x, y, button, pressed):
        self.send({
            "type": "mouse_click",
            "x": x,
            "y": y,
            "button": button.name,
            "pressed": pressed
        })

    def on_scroll(self, x, y, dx, dy):
        self.send({
            "type": "mouse_scroll",
            "dx": dx,
            "dy": dy
        })

    # --- CLAVIER ---
    def on_press(self, key):
        self.send({"type": "key_press", "key": str(key)})

    def on_release(self, key):
        self.send({"type": "key_release", "key": str(key)})

    def start(self):
        mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        ).start()

        keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        ).start()
