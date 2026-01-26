import cv2
import numpy as np

def decode_frame(data):
    # convertir les données reçues en tableau numpy (= tableau d'octets)
    np_data = np.frombuffer(data, dtype=np.uint8)
    # décoder l'image à partir du tableau numpy
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    return frame
