import cv2
from config.settings import JPEG_QUALITY

def encode_frame(frame):
    # Encodage JPEG avec OpenCV
    success, encoded = cv2.imencode(
        ".jpg",
        frame,
        [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY]
    )

    if not success:
        return None

    # IMPORTANT : convertir en bytes
    return encoded.tobytes()
