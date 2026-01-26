"""
network.py
----------
Gestion bas niveau du réseau (TCP).
AUCUNE logique métier ici (pas de capture, pas d'image).
"""

import socket          # Communication réseau
import struct          # Conversion int -> bytes
from config.settings import SERVER_IP, SERVER_PORT


def create_server():
    """
    Crée et configure le socket serveur
    """

    # Création du socket TCP IPv4
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permet de relancer le serveur sans attendre
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Association IP + port
    server_socket.bind((SERVER_IP, SERVER_PORT))

    # Mise en écoute (1 seul client)
    server_socket.listen(1)

    print(f"[SERVER] En écoute sur {SERVER_IP}:{SERVER_PORT}")

    return server_socket


def accept_client(server_socket):
    """
    Attend la connexion d’un client
    """
    return server_socket.accept()


def send_frame(client_socket, data):
    """
    Envoie une image encodée au client

    Étapes :
    1. envoyer la taille de l’image (4 octets)
    2. envoyer les données de l’image
    """

    # Taille de l’image encodée (en octets)
    size = len(data)

    # Envoi de la taille (entier non signé, big-endian)
    client_socket.sendall(struct.pack(">I", size))

    # Envoi de l’image elle-même
    client_socket.sendall(data)
