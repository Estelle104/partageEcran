import cv2
import numpy as np
import mss
from config.settings import WIDTH, HEIGHT

def get_frame():
    """Capture l'écran et le redimensionne selon WIDTH/HEIGHT
    Si WIDTH ou HEIGHT est None, utilise la résolution native"""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        # Si WIDTH/HEIGHT sont définis, redimensionner
        if WIDTH is not None and HEIGHT is not None:
            img = cv2.resize(img, (WIDTH, HEIGHT))
        
        return img
