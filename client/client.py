import cv2
from config.settings import SERVER_IP, SERVER_PORT
from client.network import connect_to_server, receive_frame
from client.display import show_frame
from client.control import send_control_request, wait_control_response, start_control_mode

def main():
    # 1. Connexion au serveur
    sock = connect_to_server(SERVER_IP, SERVER_PORT)
    print("[CLIENT] Connecté au serveur")
    print("[CLIENT] Appuyez sur 'p' pour demander le contrôle")
    print("[CLIENT] Appuyez sur 'q' pour quitter")

    has_control = False

    # 2. Boucle principale de réception vidéo
    while True:
        frame = receive_frame(sock)
        if frame is None:
            print("[CLIENT] Connexion interrompue")
            break

        key = show_frame(frame, sock)

        # Demander le contrôle
        if key == ord('p') and not has_control:
            print("[CLIENT] Demande du contrôle...")
            send_control_request(sock)
            if wait_control_response(sock):
                print("[CLIENT] Contrôle accordé!")
                has_control = True
                try:
                    start_control_mode(sock)
                except KeyboardInterrupt:
                    pass
                has_control = False
            else:
                print("[CLIENT] Contrôle refusé")

        # Quitter proprement
        if key == ord('q'):
            break

    # 3. Fermeture du socket et de OpenCV
    sock.close()
    cv2.destroyAllWindows()
    print("[CLIENT] Fermé")

if __name__ == "__main__":
    main()
