def send_permission_request(sock):
    sock.sendall(b"REQ_CONTROL")
    response = sock.recv(1024)

    if response == b"PERMISSION_GRANTED":
        print("[CLIENT] Permission accordée")
    else:
        print("[CLIENT] Permission refusée")
