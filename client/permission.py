# client/permission.py
import socket

def send_permission_request(sock):
    """
    Envoie une demande de permission au serveur.
    Cette fonction est appelée UNE SEULE FOIS au démarrage du client.
    """
    try:
        sock.sendall(b"REQ_CONTROL")
        print("[CLIENT] Demande de permission envoyée")
    except Exception as e:
        print("[CLIENT] Erreur envoi permission :", e)


def handle_permission_response(sock):
    """
    Attend la réponse du serveur concernant la permission.
    Le serveur décide : ACCEPTER ou REFUSER.
    """
    try:
        response = sock.recv(1024)

        if response == b"PERMISSION_GRANTED":
            print("[CLIENT] Permission accordée")
            return True

        elif response == b"PERMISSION_DENIED":
            print("[CLIENT] Permission refusée")
            return False

        else:
            print("[CLIENT] Réponse inconnue :", response)
            return False

    except Exception as e:
        print("[CLIENT] Erreur réception permission :", e)
        return False
