from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key
import json

mouse = MouseController()
keyboard = KeyboardController()

class InputApply:

    def handle(self, data):
        # Décoder les bytes en string si nécessaire
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        event = json.loads(data)

        if event["type"] == "mouse_move":
            mouse.position = (event["x"], event["y"])

        elif event["type"] == "mouse_click":
            btn = Button.left if event["button"] == "left" else Button.right
            if event["pressed"]:
                mouse.press(btn)
            else:
                mouse.release(btn)

        elif event["type"] == "mouse_scroll":
            mouse.scroll(event["dx"], event["dy"])

        elif event["type"] == "key_press":
            key = self.parse_key(event["key"])
            keyboard.press(key)

        elif event["type"] == "key_release":
            key = self.parse_key(event["key"])
            keyboard.release(key)

    def parse_key(self, key):
        if key.startswith("Key."):
            return getattr(Key, key.split(".")[1])
        return key.strip("'")
