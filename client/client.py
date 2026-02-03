from config.settings import SERVER_IP, SERVER_PORT
from client.network import connect_to_server, receive_frame
from client.display import show_frame
from client.permission import (
    send_permission_request,
    handle_permission_response
)

def main():
    # 1. Connexion au serveur
    sock = connect_to_server(SERVER_IP, SERVER_PORT)

    # 2. Demande de permission (UNE SEULE FOIS)
    send_permission_request(sock)
    handle_permission_response(sock)

    # 3. Boucle principale de réception vidéo
    while True:
        frame = receive_frame(sock)
        if frame is None:
            print("[CLIENT] Connexion interrompue")
            break

        key = show_frame(frame, sock)

        # Quitter proprement
        if key == ord('q'):
            break

    # 4. Fermeture du socket
    sock.close()
    print("[CLIENT] Fermé")

if __name__ == "__main__":
    main()
