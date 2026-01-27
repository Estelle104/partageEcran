import cv2
import numpy as np
import mss
from config.settings import WIDTH, HEIGHT

def get_frame():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = np.array(sct.grab(monitor))
        img = cv2.resize(img, (WIDTH, HEIGHT))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img