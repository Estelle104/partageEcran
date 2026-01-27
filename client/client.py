from config.settings import SERVER_IP, SERVER_PORT
from client.network import connect_to_server, receive_frame
from client.decoder import decode_frame
from client.display import show_frame
from client.input_capture import InputCapture


def main():
    sock = connect_to_server(SERVER_IP, SERVER_PORT)

    input_capture = InputCapture(sock)
    input_capture.start()

    while True:
        frame_data = receive_frame(sock)
        if frame_data is None:
            break

        frame = decode_frame(frame_data)
        key = show_frame(frame)

        if key == ord('q'):
            break

    sock.close()


if __name__ == "__main__":
    main()
