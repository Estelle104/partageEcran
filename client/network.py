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
    """Receive a single full-frame JPEG from server.
    Server sends: [len:>I][jpeg bytes]
    Returns decoded BGR `numpy` image or None on error.
    """
    # Read length (4 bytes)
    hdr = _recv_exact(sock, 4)
    if not hdr:
        return None

    try:
        l = struct.unpack(">I", hdr)[0]
    except struct.error:
        return None

    data = _recv_exact(sock, l)
    if not data:
        return None

    np_data = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
    return frame
