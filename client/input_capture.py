from pynput import mouse, keyboard
import json
import struct
from common.protocol import MSG_INPUT


class InputCapture:
    def __init__(self, network):
        self.network = network
        self.running = True

    def send(self, data):
        """Envoie les données d'entrée au serveur"""
        try:
            json_data = json.dumps(data).encode()
            # Format: [msg_type:>B][size:>I][json_data]
            msg_type = struct.pack(">B", MSG_INPUT)
            size = struct.pack(">I", len(json_data))
            self.network.sendall(msg_type + size + json_data)
        except Exception as e:
            print(f"[CLIENT] Erreur envoi entrée: {e}")
            self.running = False

    # --- SOURIS ---
    def on_move(self, x, y):
        if self.running:
            self.send({"type": "mouse_move", "x": x, "y": y})

    def on_click(self, x, y, button, pressed):
        if self.running:
            self.send({
                "type": "mouse_click",
                "x": x,
                "y": y,
                "button": button.name,
                "pressed": pressed
            })

    def on_scroll(self, x, y, dx, dy):
        if self.running:
            self.send({
                "type": "mouse_scroll",
                "dx": dx,
                "dy": dy
            })

    # --- CLAVIER ---
    def on_press(self, key):
        if self.running:
            self.send({"type": "key_press", "key": str(key)})

    def on_release(self, key):
        if self.running:
            self.send({"type": "key_release", "key": str(key)})

    def start(self):
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        self.mouse_listener.start()

        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.keyboard_listener.start()
    
    def stop(self):
        self.running = False
        if hasattr(self, 'mouse_listener'):
            self.mouse_listener.stop()
        if hasattr(self, 'keyboard_listener'):
            self.keyboard_listener.stop()
