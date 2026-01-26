import cv2          # Affichage et traitement image
import numpy as np  # Manipulation tableau image
import mss          # Capture écran rapide

# Taille de l image configuré dans config.settings
from config.settings import WIDTH, HEIGHT

# Capture propre avec 'with'. monitors[1]: écran principale
with mss.mss() as sct:
    monitor = sct.monitors[1]
    while True:
        # Capture ecran et conversion en tableau numPy
        img = np.array(sct.grab(monitor))
        # Optimisation majeure et reduit la charge Cpu et reseau
        img = cv2.resize(img, (WIDTH, HEIGHT))
        # Conversion proprement de l image
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        # test visuel immédiat
        cv2.imshow("Capture ecran", img)
        # Sortie
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
