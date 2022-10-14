import datetime as dt
import socket
import time


def socket_client_tcp():
    print("socket client tcp")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(("localhost", 5000))

        client.send(f"{dt.datetime.now()}: Hello Server!".encode("utf-8"))
        # time.sleep(0.1)

        print(client.recv(1024).decode("utf-8"))
        # time.sleep(0.1)

        client.send(f"{dt.datetime.now()}: Bye Server!".encode("utf-8"))
        # time.sleep(0.1)

        print(client.recv(1024).decode("utf-8"))

    print("")


def socket_client_udp():
    print("socket client udp")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:

        message = f"{dt.datetime.now()}: Hello Server!".encode("utf-8")
        client.sendto(message, ("localhost", 5001))
        print(client.recvfrom(1024)[0].decode("utf-8"))

        message = f"{dt.datetime.now()}: Bye Server!".encode("utf-8")
        client.sendto(message, ("localhost", 5001))
        print(client.recvfrom(1024)[0].decode("utf-8"))

    print("")


def main():
    socket_client_tcp()
    socket_client_udp()


if __name__ == "__main__":
    main()


# cd "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste Socket TCP vs UDP"
# python client.py
