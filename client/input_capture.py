from pynput import mouse, keyboard
import json
import struct
import time
from common.protocol import MSG_INPUT


class InputCapture:
    def __init__(self, network):
        self.network = network
        self.running = True
        self.last_move_time = 0
        self.move_throttle = 0.05  # Envoyer le mouvement max tous les 50ms

    def send(self, data):
        """Envoie les données d'entrée au serveur"""
        if not self.running:
            return
            
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
        """Mouvement de souris avec throttling pour éviter surcharge"""
        if not self.running:
            return
        
        now = time.time()
        if now - self.last_move_time >= self.move_throttle:
            self.send({"type": "mouse_move", "x": x, "y": y})
            self.last_move_time = now

    def on_click(self, x, y, button, pressed):
        if self.running:
            try:
                self.send({
                    "type": "mouse_click",
                    "x": x,
                    "y": y,
                    "button": button.name,
                    "pressed": pressed
                })
            except Exception as e:
                print(f"[CLIENT] Erreur click souris: {e}")
                self.running = False

    def on_scroll(self, x, y, dx, dy):
        if self.running:
            try:
                self.send({
                    "type": "mouse_scroll",
                    "dx": dx,
                    "dy": dy
                })
            except Exception as e:
                print(f"[CLIENT] Erreur scroll: {e}")
                self.running = False

    # --- CLAVIER ---
    def on_press(self, key):
        if self.running:
            try:
                self.send({"type": "key_press", "key": str(key)})
            except Exception as e:
                print(f"[CLIENT] Erreur key_press: {e}")
                self.running = False

    def on_release(self, key):
        if self.running:
            try:
                self.send({"type": "key_release", "key": str(key)})
            except Exception as e:
                print(f"[CLIENT] Erreur key_release: {e}")
                self.running = False

    def start(self):
        try:
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
            print("[CLIENT] Capture d'entrées démarrée")
        except Exception as e:
            print(f"[CLIENT] Erreur au démarrage de la capture: {e}")
            self.running = False
    
    def stop(self):
        self.running = False
        try:
            if hasattr(self, 'mouse_listener'):
                self.mouse_listener.stop()
            if hasattr(self, 'keyboard_listener'):
                self.keyboard_listener.stop()
            print("[CLIENT] Capture d'entrées arrêtée")
        except Exception as e:
            print(f"[CLIENT] Erreur arrêt capture: {e}")
