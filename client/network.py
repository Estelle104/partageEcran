import socket
import struct
import cv2
import numpy as np

# Persistent frame buffer to keep unchanged pixels between updates
_current_frame = None


def connect_to_server(server_ip, server_port, timeout=5):
    # If config contains 0.0.0.0 (used for server bind), use localhost for client
    host = server_ip
    if host == "0.0.0.0":
        host = "127.0.0.1"

    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((host, server_port))
    except Exception as e:
        # Try an explicit localhost fallback if first attempt failed
        if host != "127.0.0.1":
            try:
                s.connect(("127.0.0.1", server_port))
            except Exception:
                s.close()
                raise
        else:
            s.close()
            raise

    s.settimeout(None)
    return s


def _recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf += chunk
    return buf


def receive_frame(sock):
    """
    Reçoit un paquet de changements envoyé par le serveur et applique
    les blocs JPEG reçus sur une image persistante. Retourne l'image
    complète (numpy array) prête à l'affichage, ou None si erreur.
    Format du paquet (serveur):
      [width:>H][height:>H][n_changes:>H]
      pour chaque changement:
        [idx:>H][x:>H][y:>H][len:>I][data...]
    """
    global _current_frame

    # Lire l'en-tête (6 octets)
    hdr = _recv_exact(sock, 6)
    if not hdr:
        return None

    try:
        w, h, n_changes = struct.unpack(">HHH", hdr)
    except struct.error:
        return None

    # Initialize buffer if needed
    if _current_frame is None or _current_frame.shape[0] != h or _current_frame.shape[1] != w:
        _current_frame = np.zeros((h, w, 3), dtype=np.uint8)

    # Read and apply each change
    for _ in range(n_changes):
        meta = _recv_exact(sock, 10)  # idx(2)+x(2)+y(2)+len(4)
        if not meta:
            return None
        idx, x, y, l = struct.unpack(">HHHI", meta)

        data = _recv_exact(sock, l)
        if not data:
            return None

        # Decode JPEG block and paste into buffer
        np_data = np.frombuffer(data, dtype=np.uint8)
        block = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        if block is None:
            continue

        bh, bw, _ = block.shape
        _current_frame[y:y+bh, x:x+bw] = block

    return _current_frame
