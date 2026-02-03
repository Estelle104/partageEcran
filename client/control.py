import struct
from common.protocol import MSG_CONTROL_REQUEST, MSG_CONTROL_RESPONSE, MSG_INPUT, MSG_RELEASE_CONTROL, CONTROL_ACCEPTED, CONTROL_REFUSED
from client.input_capture import InputCapture


def send_control_request(sock):
    """
    Envoie une demande de contrôle au serveur
    """
    msg = struct.pack(">B", MSG_CONTROL_REQUEST)
    sock.sendall(msg)


def wait_control_response(sock):
    """
    Attend la réponse du serveur pour la demande de contrôle
    Retourne True si contrôle accepté, False sinon
    """
    try:
        response = sock.recv(2)
        if len(response) < 2:
            return False
        
        msg_type = struct.unpack(">B", response[0:1])[0]
        status = struct.unpack(">B", response[1:2])[0]
        
        if msg_type == MSG_CONTROL_RESPONSE:
            if status == CONTROL_ACCEPTED:
                return True
            else:
                return False
    except Exception as e:
        print(f"[CLIENT] Erreur lors de la réception de la réponse: {e}")
        return False


def start_control_mode(sock):
    """
    Démarre le mode contrôle: capture et envoie les entrées au serveur
    """
    print("[CLIENT] Mode contrôle activé")
    print("[CLIENT] Appuyez sur 'CTRL+C' pour libérer le contrôle")
    
    input_capture = InputCapture(sock)
    input_capture.start()
    
    try:
        # Bloque jusqu'à interruption
        while True:
            pass
    except KeyboardInterrupt:
        print("\n[CLIENT] Libération du contrôle...")
        release_control(sock)


def release_control(sock):
    """
    Libère le contrôle et l'envoie au serveur
    """
    msg = struct.pack(">B", MSG_RELEASE_CONTROL)
    size = struct.pack(">I", len(msg))
    try:
        sock.sendall(size + msg)
    except:
        pass
    print("[CLIENT] Contrôle libéré")
