import socket, struct, threading
from server.screen_capture import get_frame
from server.block_diff import diff_blocks
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
    prev_hashes = {}

    while True:
        frame = get_frame()
        if frame is None:
            continue

        changes = diff_blocks(prev_hashes, frame)

        h, w, _ = frame.shape

        # Packet: [width:>H][height:>H][n_changes:>H][changes...]
        packet = struct.pack(">HHH", w, h, len(changes))
        for idx, x, y, data in changes:
            packet += struct.pack(">HHHI", idx, x, y, len(data))
            packet += data

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
