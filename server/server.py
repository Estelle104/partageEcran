import socket, struct, threading
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


clients = {}
lock = threading.Lock()
controller = None   # client autorisé à contrôler

def handle_client(sock, addr):
    global controller
    print(f"[CLIENT] connecté {addr}")

    with lock:
        clients[sock] = {}

    try:
        while True:
            msg = sock.recv(32)
            if not msg:
                break

            if msg == b"REQ_CONTROL":
                print("[SERVER] Demande de contrôle reçue")
                decision = input("Autoriser ? (y/n) : ")
                if decision == "y":
                    controller = sock
                    sock.sendall(b"PERMISSION_GRANTED")
                else:
                    sock.sendall(b"PERMISSION_DENIED")

    finally:
        with lock:
            clients.pop(sock, None)
        sock.close()
        print(f"[CLIENT] déconnecté {addr}")

def broadcast():
    """Broadcast full JPEG frames to all connected clients.
    This sends a length-prefixed JPEG per frame which favors fluidity.
    Packet format: [len:>I][jpeg bytes]
    """
    while True:
        frame = get_frame()
        if frame is None:
            continue

        data = encode_frame(frame)
        if data is None:
            continue

        packet = struct.pack(">I", len(data)) + data

        with lock:
            for c in list(clients.keys()):
                try:
                    c.sendall(packet)
                except:
                    clients.pop(c, None)

def start_server():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((SERVER_IP, SERVER_PORT))
    s.listen()
    print(f"[SERVER] écoute sur {SERVER_IP}:{SERVER_PORT}")

    threading.Thread(target=broadcast, daemon=True).start()

    while True:
        sock, addr = s.accept()
        threading.Thread(target=handle_client, args=(sock, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
