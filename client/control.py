import struct
import threading
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


# Variable globale pour gérer l'état du contrôle
_control_active = False
_input_capture = None


def start_control_mode(sock):
    """
    Démarre le mode contrôle: capture et envoie les entrées au serveur
    Lance la capture d'entrées en thread séparé pour que la vidéo continue
    """
    global _control_active, _input_capture
    
    print("[CLIENT] Mode contrôle activé")
    print("[CLIENT] Appuyez sur 'CTRL+C' pour libérer le contrôle")
    
    _control_active = True
    _input_capture = InputCapture(sock)
    
    # Lance la capture d'entrées en thread séparé
    capture_thread = threading.Thread(target=_input_capture.start, daemon=True)
    capture_thread.start()
    
    # Retourne immédiatement pour que la boucle vidéo continue


def stop_control_mode(sock):
    """
    Arrête le mode contrôle
    """
    global _control_active, _input_capture
    
    _control_active = False
    if _input_capture:
        _input_capture.running = False
    
    release_control(sock)


def release_control(sock):
    """
    Libère le contrôle et l'envoie au serveur
    """
    # Format: [size:>I][msg_type:>B]
    msg_type = struct.pack(">B", MSG_RELEASE_CONTROL)
    size = struct.pack(">I", 1)  # Taille = 1 byte (juste le type de message)
    try:
        sock.sendall(size + msg_type)
    except:
        pass
    print("[CLIENT] Contrôle libéré")
