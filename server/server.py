"""
server.py
---------
Serveur principal de partage d'écran
"""

from server.network import create_server, accept_client, send_frame
from server.screen_capture import get_frame
from server.encoder import encode_frame


def start_server():
    # 1️⃣ Création du serveur réseau
    server_socket = create_server()

    print("[SERVER] En attente d'un client...")
    client_socket, client_address = accept_client(server_socket)
    print(f"[SERVER] Client connecté : {client_address}")

    # 2️⃣ Boucle d'envoi des images
    while True:
        frame = get_frame()
        if frame is None:
            continue

        encoded = encode_frame(frame)
        if encoded is None:
            continue

        send_frame(client_socket, encoded)


if __name__ == "__main__":
    start_server()
