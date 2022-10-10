import socket
import struct
import time


def main():

    host = socket.gethostname()  # "localhost"
    port = 5000  # 8888  # 5000

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    client, addr = server.accept()
    print("Connection from: " + str(addr))

    with client:
        print(f"Connected by {addr}")
        while True:
            data = client.recv(1024)
            if not data:
                break
            first, last, age, gender, occupstion, weight = struct.unpack(
                "10s 10s i s 15s f", data
            )
            print(
                first.decode().rstrip("\x00"),
                last.decode().rstrip("\x00"),
                age,
                gender.decode().rstrip("\x00"),
                occupstion.decode().rstrip("\x00"),
                weight,
            )

    server.close()


if __name__ == "__main__":
    main()


# cd "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste Packaginging Structs"
# python server.py
