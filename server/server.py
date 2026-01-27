import socket
import struct
import threading

from server.screen_capture import get_frame
from server.encoder import encode_frame
from config.settings import SERVER_IP, SERVER_PORT
from server.input_apply import InputApply


def input_loop(client_socket):
    while True:
        size_data = client_socket.recv(4)
        if not size_data:
            break

        size = struct.unpack(">I", size_data)[0]
        data = client_socket.recv(size)
        input_apply.handle(data)


def screen_loop(client_socket):
    while True:
        frame = get_frame()
        if frame is None:
            continue

        data = encode_frame(frame)
        if data is None:
            continue

        client_socket.sendall(struct.pack(">I", len(data)))
        client_socket.sendall(data)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(1)

    print(f"[SERVER] En attente de connexion sur {SERVER_IP}:{SERVER_PORT}")
    client_socket, addr = server_socket.accept()
    print(f"[SERVER] Client connecté depuis {addr}")

    try:
        t1 = threading.Thread(target=input_loop, args=(client_socket,), daemon=True)
        t2 = threading.Thread(target=screen_loop, args=(client_socket,), daemon=True)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    finally:
        client_socket.close()
        server_socket.close()


if __name__ == "__main__":
    start_server()
