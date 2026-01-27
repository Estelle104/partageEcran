import struct
from common.protocol import MSG_CONTROL_REQUEST

def send_control_request(sock):
    """
    Envoie une demande de contrôle au serveur
    """
    # Message = [type=1 octet]
    msg = struct.pack(">B", MSG_CONTROL_REQUEST)
    sock.sendall(msg)
