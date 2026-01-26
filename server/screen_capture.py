import cv2          # Affichage et traitement image
import numpy as np  # Manipulation tableau image
import mss          # Capture écran rapide

# Taille de l'image configurée dans config.settings
from config.settings import WIDTH, HEIGHT
# Import de la fonction d'encodage
from server.encoder import encode_frame


with mss.mss() as sct:
    monitor = sct.monitors[1]

    while True:
        # Capture écran et conversion en tableau NumPy
        img = np.array(sct.grab(monitor))

        # Optimisation majeure : réduction CPU et réseau
        img = cv2.resize(img, (WIDTH, HEIGHT))

        # Conversion BGRA -> BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # Encodage JPEG
        data = encode_frame(img)

        if data is None:
            continue

        print(f"Taille image encodée: {len(data)} octets")

        # (Affichage volontairement désactivé côté serveur)
        # cv2.imshow("Capture ecran", img)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

cv2.destroyAllWindows()
