import socket, struct, threading
from server.screen_capture import get_frame
from server.encoder import encode_frame
from config.settings import SERVER_IP, SERVER_PORT
from server.input_apply import InputApply
from common.protocol import MSG_CONTROL_REQUEST, MSG_CONTROL_RESPONSE, MSG_INPUT, MSG_RELEASE_CONTROL, CONTROL_ACCEPTED, CONTROL_REFUSED


input_apply = InputApply()
clients = {}
lock = threading.Lock()
controller = None   # client autorisé à contrôler


def handle_input_from_controller(client_socket):
    """Reçoit les entrées du client qui contrôle"""
    global controller
    while controller == client_socket:
        try:
            # Reçoit la taille du message
            size_data = client_socket.recv(4)
            if not size_data:
                break
            
            size = struct.unpack(">I", size_data)[0]
            if size == 0:
                break
            
            # Reçoit le message d'entrée
            msg_type_data = client_socket.recv(1)
            if not msg_type_data:
                break
            
            msg_type = struct.unpack(">B", msg_type_data)[0]
            
            # Reçoit les données d'entrée
            input_data = client_socket.recv(size - 1)
            if not input_data:
                break
            
            # Si c'est une libération de contrôle
            if msg_type == MSG_RELEASE_CONTROL:
                with lock:
                    if controller == client_socket:
                        controller = None
                print("[SERVER] Contrôle libéré")
                break
            
            # Si c'est une entrée
            elif msg_type == MSG_INPUT:
                input_apply.handle(input_data)
        
        except Exception as e:
            print(f"[SERVER] Erreur lors de la réception d'entrée: {e}")
            break
    
    # Libère le contrôle si le client se déconnecte
    with lock:
        if controller == client_socket:
            controller = None


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


def handle_client(sock, addr):
    global controller
    print(f"[CLIENT] connecté {addr}")

    with lock:
        clients[sock] = {"addr": addr, "controlled": False}

    try:
        while True:
            try:
                # Reçoit le type de message (1 byte)
                msg_type_data = sock.recv(1)
                if not msg_type_data:
                    print(f"[SERVER] {addr} a fermé la connexion")
                    break
                
                msg_type = struct.unpack(">B", msg_type_data)[0]
                
                # Demande de contrôle du client
                if msg_type == MSG_CONTROL_REQUEST:
                    print(f"[SERVER] Demande de contrôle reçue de {addr}")
                    with lock:
                        if controller is None:
                            # Demande à l'utilisateur
                            decision = input(f"Autoriser {addr} à contrôler ? (y/n) : ")
                            if decision.lower() == "y":
                                controller = sock
                                response = struct.pack(">B", MSG_CONTROL_RESPONSE) + struct.pack(">B", CONTROL_ACCEPTED)
                                sock.sendall(response)
                                print(f"[SERVER] {addr} a obtenu le contrôle")
                            else:
                                response = struct.pack(">B", MSG_CONTROL_RESPONSE) + struct.pack(">B", CONTROL_REFUSED)
                                sock.sendall(response)
                                print(f"[SERVER] {addr} a été refusé")
                        else:
                            # Un client contrôle déjà
                            response = struct.pack(">B", MSG_CONTROL_RESPONSE) + struct.pack(">B", CONTROL_REFUSED)
                            sock.sendall(response)
                            print(f"[SERVER] {addr} refusé (contrôle déjà actif)")
                
                # Message d'entrée du contrôleur
                elif msg_type == MSG_INPUT:
                    if controller == sock:
                        # Reçoit la taille du message (4 bytes)
                        size_data = sock.recv(4)
                        if not size_data or len(size_data) < 4:
                            print(f"[SERVER] Erreur: taille manquante pour MSG_INPUT")
                            break
                        
                        size = struct.unpack(">I", size_data)[0]
                        
                        # Reçoit les données d'entrée
                        input_data = b""
                        while len(input_data) < size:
                            chunk = sock.recv(size - len(input_data))
                            if not chunk:
                                print(f"[SERVER] Connexion fermée lors de la réception de MSG_INPUT")
                                break
                            input_data += chunk
                        
                        if len(input_data) == size:
                            try:
                                input_apply.handle(input_data)
                            except Exception as e:
                                print(f"[SERVER] Erreur application entrée: {e}")
                
                # Libération du contrôle
                elif msg_type == MSG_RELEASE_CONTROL:
                    with lock:
                        if controller == sock:
                            controller = None
                            print(f"[SERVER] Contrôle libéré par {addr}")
            
            except struct.error as e:
                print(f"[SERVER] Erreur struct pour {addr}: {e}")
                break
            except Exception as e:
                print(f"[SERVER] Erreur réception message de {addr}: {e}")
                break

    finally:
        with lock:
            if controller == sock:
                controller = None
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
