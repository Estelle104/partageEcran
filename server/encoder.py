import cv2

# frame : image OpenCV (ndarray)
def encode_frame(frame, quality=50):
    """
    Encode une image OpenCV en JPEG compressé.
    quality : 1 (très compressé) -> 100 (meilleure qualité)
    """
    # Paramètres d'encodage JPEG
    encode_params = [
        int(cv2.IMWRITE_JPEG_QUALITY),
        quality
    ]
    # encode l'image en memoire, en jpeg avec les parametres donnés
    success, encoded_image = cv2.imencode(".jpg", frame, encode_params)

    if not success:
        return None

    # Convertit l'image encodée en bytes pour l'envoi réseau
    return encoded_image.tobytes()
