import datetime as dt
import socket
import time


def socket_server_tcp():
    print("socket server tcp")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 5000))
        server.listen()

        # while True:
        client, address = server.accept()
        print(f"Connected to {address}")

        print(client.recv(1024).decode("utf-8"))
        # time.sleep(0.1)

        client.send(f"{dt.datetime.now()}: Hello Client!".encode("utf-8"))
        # time.sleep(0.1)

        print(client.recv(1024).decode("utf-8"))
        # time.sleep(0.1)

        client.send(f"{dt.datetime.now()}: Bye Client!".encode("utf-8"))
        # time.sleep(0.1)

    print("")


def socket_server_udp():
    print("socket server udp")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind(("localhost", 5001))

        # while True:
        message, address = server.recvfrom(1024)
        print(message.decode("utf-8"))
        server.sendto(f"{dt.datetime.now()}: Hello Client!".encode("utf-8"), address)

        message, address = server.recvfrom(1024)
        print(message.decode("utf-8"))
        server.sendto(f"{dt.datetime.now()}: Bye Client!".encode("utf-8"), address)

    print("")


def main():
    socket_server_tcp()
    socket_server_udp()


if __name__ == "__main__":
    main()


# cd "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste Socket TCP vs UDP"
# python server.py
