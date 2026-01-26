import socket          # Module pour la communication réseau (TCP/IP)
import struct          # Permet de convertir des entiers en bytes
import time            # Pour contrôler la vitesse si besoin

# Import de la capture écran
from server.screen_capture import get_frame
# Import de l'encodeur JPEG
from server.encoder import encode_frame
# Paramètres réseau
from config.settings import SERVER_IP, SERVER_PORT


def start_server():
    # Création du socket TCP (IPv4)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Autorise la réutilisation de l'adresse (évite "Address already in use")
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Associe le socket à l'IP et au port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Met le serveur en mode écoute (1 client max)
    server_socket.listen(1)

    print(f"[SERVER] En attente de connexion sur {SERVER_IP}:{SERVER_PORT}...")

    # Attend qu'un client se connecte
    client_socket, client_address = server_socket.accept()
    print(f"[SERVER] Client connecté : {client_address}")

    try:
        # Boucle principale : envoi des frames en continu
        while True:
            # Capture une image écran (OpenCV / numpy)
            frame = get_frame()

            # Si la capture a échoué, on passe
            if frame is None:
                continue

            # Encode l'image en JPEG compressé
            encoded_frame = encode_frame(frame)

            # Si l'encodage a échoué, on passe
            if encoded_frame is None:
                continue

            # Taille de l'image encodée (en octets)
            frame_size = len(encoded_frame)

            # On envoie d'abord la taille (4 octets, entier non signé)
            client_socket.sendall(struct.pack(">I", frame_size))

            # Puis on envoie les données de l'image
            client_socket.sendall(encoded_frame)

            # Petite pause optionnelle pour limiter le CPU (ex: 60 FPS max)
            # time.sleep(0.016)

    except Exception as e:
        print("[SERVER] Erreur :", e)

    finally:
        # Fermeture propre des sockets
        client_socket.close()
        server_socket.close()
        print("[SERVER] Connexion fermée")


# Point d'entrée du programme
if __name__ == "__main__":
    start_server()
