import cv2
from client.permission import send_permission_request

def show_frame(frame, sock=None):
    cv2.imshow("Partage écran", frame)
    key = cv2.waitKey(1) & 0xFF

    # Appuyer sur "p" pour demander la permission
    if key == ord("p") and sock is not None:
        send_permission_request(sock)

    return key
