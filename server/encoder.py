import cv2
from config.settings import JPEG_QUALITY

def encode_frame(frame):
    ret, buffer = cv2.imencode(
        ".jpg",
        frame,
        [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]
    )
    if not ret:
        return None
    return buffer.tobytes()
