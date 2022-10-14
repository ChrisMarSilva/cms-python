import datetime as dt
import socket
import time


def simply_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(("localhost", 5000))

        data = f"DtHr: {dt.datetime.now()}"
        client.send(data.encode("utf-8"))

        data = client.recv(1024)
        print(data.decode("utf-8"))


def thread_client():

    HEADER = 64
    FORMAT = "utf-8"
    DISCONNECT_MESSAGE = "!DISCONNECT"
    SERVER = socket.gethostbyname(
        socket.gethostname()
    )  # "localhost"  # "192.168.1.109"  # "192.168.1.26"
    PORT = 5000
    ADDR = (SERVER, PORT)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(ADDR)

        def send(msg):
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b" " * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
            print(client.recv(2048).decode(FORMAT))

        send("Hello World!")
        input()
        send("Hello Everyone!")
        input()
        send("Hello Tim!")
        send(DISCONNECT_MESSAGE)


def main():
    # simply_client()
    thread_client()


if __name__ == "__main__":
    main()


# cd "C:\Users\chris\Desktop\CMS Python\CMS Teste API e Web\CMS Teste Socket Simply Explained"
# python client.py
