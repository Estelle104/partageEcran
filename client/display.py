import cv2

def show_frame(frame):
    # afficher l'image dans une fenêtre nommée "Ecran distant"
    cv2.imshow("Ecran distant", frame)
    # attendre 1 ms pour permettre la mise à jour de la fenêtre
    return cv2.waitKey(1) & 0xFF
