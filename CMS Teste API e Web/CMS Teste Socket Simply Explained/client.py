import datetime as dt
import socket
import time


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(("localhost", 5000))

        data = f"DtHr: {dt.datetime.now()}"
        client.send(data.encode("utf-8"))

        data = client.recv(1024)
        print(data.decode("utf-8"))


if __name__ == "__main__":
    main()


# cd "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste Socket Simply Explained"
# python client.py
