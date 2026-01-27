import socket
import struct

# ---------------------------
# Connexion au serveur
# ---------------------------
def connect_to_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    return sock


# ---------------------------
# Permission de contrôle
# ---------------------------
def send_permission_request(sock):
    sock.sendall(b"REQ_CONTROL")
    response = sock.recv(1024)

    if response == b"PERMISSION_GRANTED":
        print("[CLIENT] Permission accordée")
        return True
    else:
        print("[CLIENT] Permission refusée")
        return False


# ---------------------------
# Réception fiable de données
# ---------------------------
def recvall(sock, size):
    data = b""
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data


# ---------------------------
# Réception d'une frame
# ---------------------------
def receive_frame(sock):
    packed_size = recvall(sock, 4)
    if not packed_size:
        return None

    frame_size = struct.unpack(">I", packed_size)[0]
    return recvall(sock, frame_size)
