import socket
import struct

from server.screen_capture import get_frame
from server.encoder import encode_frame
from config.settings import SERVER_IP, SERVER_PORT

def start_server():
    # 1. Création du socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. Bind IP + port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # 3. Mise en écoute
    server_socket.listen(1)
    print(f"[SERVER] En attente de connexion sur {SERVER_IP}:{SERVER_PORT}")

    # 4. Attente du client
    client_socket, addr = server_socket.accept()
    print(f"[SERVER] Client connecté depuis {addr}")

    try:
        while True:
            # Capture écran
            frame = get_frame()
            if frame is None:
                continue

            # Encodage JPEG
            data = encode_frame(frame)
            if data is None:
                continue

            # Envoi taille + image
            client_socket.sendall(struct.pack(">I", len(data)))
            client_socket.sendall(data)

            print("Bind sur", SERVER_IP, SERVER_PORT)
            server_socket.bind((SERVER_IP, SERVER_PORT))
            print("Listen...")
            server_socket.listen(1)
            print("Accept...")
            client_socket, addr = server_socket.accept()
            print("Client connecté", addr)

    except Exception as e:
        print("[SERVER] Erreur :", e)

    finally:
        client_socket.close()
        server_socket.close()
        print("[SERVER] Serveur arrêté")

if __name__ == "__main__":
    start_server()
