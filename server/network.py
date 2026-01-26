import socket
import struct
from config.settings import SERVER_IP, SERVER_PORT


def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(1)
    print(f"[SERVER] En écoute sur {SERVER_IP}:{SERVER_PORT}")
    return server_socket


def accept_client(server_socket):
    return server_socket.accept()


def send_frame(client_socket, data):
    size = len(data)
    client_socket.sendall(struct.pack(">I", size))
    client_socket.sendall(data)
