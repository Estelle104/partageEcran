from config.settings import SERVER_IP, SERVER_PORT
from client.network import connect_to_server, receive_frame
from client.decoder import decode_frame
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
        frame_data = receive_frame(sock)
        if frame_data is None:
            print("[CLIENT] Connexion interrompue")
            break

        frame = decode_frame(frame_data)
        key = show_frame(frame)

        # Quitter proprement
        if key == ord('q'):
            break

    # 4. Fermeture du socket
    sock.close()
    print("[CLIENT] Fermé")

if __name__ == "__main__":
    main()
