import socket
import struct


def recvall(sock, size):
    """
    Reçoit EXACTEMENT 'size' octets depuis le socket.
    TCP peut envoyer les données en plusieurs morceaux,
    donc on boucle jusqu'à tout recevoir.
    """
    data = b""  # Buffer vide pour stocker les données reçues

    while len(data) < size:
        # On reçoit le reste des octets manquants
        packet = sock.recv(size - len(data))

        # Si recv retourne vide => connexion fermée par le serveur
        if not packet:
            return None

        # On ajoute les données reçues au buffer
        data += packet

    # Quand on a reçu exactement 'size' octets
    return data


def connect_to_server(ip, port):
    """
    Crée un socket TCP et se connecte au serveur
    identifié par son IP et son port.
    """
    # Création du socket :
    # AF_INET  -> IPv4
    # SOCK_STREAM -> TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connexion au serveur
    sock.connect((ip, port))

    return sock


def receive_frame(sock):
    """
    Reçoit une image envoyée par le serveur.
    Protocole utilisé :
    1) 4 octets : taille de l'image (entier non signé)
    2) N octets : données réelles de l'image
    """

    # --- Étape 1 : lire la taille de l'image ---

    # On lit exactement 4 octets
    packed_size = recvall(sock, 4)

    # Si rien reçu => connexion coupée
    if not packed_size:
        return None

    # Conversion des 4 octets en entier
    # ">I" :
    #   >  : big-endian (ordre réseau)
    #   I  : unsigned int (4 octets)
    frame_size = struct.unpack(">I", packed_size)[0]

    # --- Étape 2 : lire les données de l'image ---

    # On reçoit exactement frame_size octets
    frame_data = recvall(sock, frame_size)

    # frame_data contient l'image brute (bytes)
    return frame_data
