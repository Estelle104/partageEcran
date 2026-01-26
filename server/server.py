import socket
import struct
import time

from server.screen_capture import get_frame
from server.encoder import encode_frame
from config.settings import SERVER_IP, SERVER_PORT

def main():
    # Création du socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permet de relancer sans attendre
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind IP + port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Écoute des connexions
    server_socket.listen(1)
    print(f"[SERVER] En attente sur {SERVER_IP}:{SERVER_PORT}")

    # Attente client
    client_socket, addr = server_socket.accept()
    print(f"[SERVER] Client connecté : {addr}")

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

            # Envoi taille (4 octets)
            client_socket.sendall(struct.pack(">I", len(data)))

            # Envoi image
            client_socket.sendall(data)

            time.sleep(0.02)  # ~50 FPS

    except Exception as e:
        print("[SERVER] Erreur:", e)

    finally:
        client_socket.close()
        server_socket.close()
        print("[SERVER] Fermé")

if __name__ == "__main__":
    main()
