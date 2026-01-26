"""
server.py
---------
Point d’entrée principal du serveur.
Il coordonne :
- la capture d’écran
- l’encodage des images
- l’envoi au client via le réseau
"""

# Import des fonctions réseau (socket)
from server.network import create_server, accept_client, send_frame

# Capture écran (retourne une image numpy / OpenCV)
from server.screen_capture import get_frame

# Encodage JPEG (compression)
from server.encoder import encode_frame


def start_server():
    """
    Démarre le serveur de partage d’écran
    """

    # 1️⃣ Création du socket serveur (TCP)
    server_socket = create_server()

    # 2️⃣ Attente d’un client
    client_socket, client_address = accept_client(server_socket)
    print(f"[SERVER] Client connecté depuis {client_address}")

    # 3️⃣ Boucle principale : streaming en continu
    while True:
        # Capture une frame écran
        frame = get_frame()

        # Si la capture échoue, on saute cette itération
        if frame is None:
            continue

        # Encode l’image (JPEG compressé)
        encoded_frame = encode_frame(frame)

        # Si l’encodage échoue, on saute
        if encoded_frame is None:
            continue

        # Envoi de la frame au client
        send_frame(client_socket, encoded_frame)


# Lancement du serveur uniquement si ce fichier est exécuté directement
if __name__ == "__main__":
    start_server()
