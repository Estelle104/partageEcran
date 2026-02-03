import cv2
from config.settings import SERVER_IP, SERVER_PORT
from client.network import connect_to_server, receive_frame
from client.display import show_frame

def main():
    # 1. Connexion au serveur
    sock = connect_to_server(SERVER_IP, SERVER_PORT)
    print("[CLIENT] Connecté au serveur")
    print("[CLIENT] Appuyez sur 'p' pour demander la permission de contrôle")
    print("[CLIENT] Appuyez sur 'q' pour quitter")

    # 2. Boucle principale de réception vidéo
    while True:
        frame = receive_frame(sock)
        if frame is None:
            print("[CLIENT] Connexion interrompue")
            break

        key = show_frame(frame, sock)

        # Quitter proprement
        if key == ord('q'):
            break

    # 3. Fermeture du socket et de OpenCV
    sock.close()
    cv2.destroyAllWindows()
    print("[CLIENT] Fermé")

if __name__ == "__main__":
    main()
