import socket, struct, threading
from server.screen_capture import get_frame
from server.block_diff import diff_blocks
from config.settings import SERVER_IP, SERVER_PORT

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

        packet = struct.pack(">H", len(changes))
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
