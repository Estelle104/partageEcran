import cv2

_window_created = False

def show_frame(frame, sock=None):
    global _window_created
    
    # Créer la fenêtre une seule fois
    if not _window_created:
        cv2.namedWindow("Partage écran", cv2.WINDOW_AUTOSIZE)
        _window_created = True
    
    cv2.imshow("Partage écran", frame)
    key = cv2.waitKey(1) & 0xFF

    return key
