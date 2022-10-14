import socket
import struct
import time


def main():
    first_name = "Chris"
    last_name = "MarSil"
    age = 20
    gender = "m"
    occupstion = "Programmer"
    weight = 54.52

    data = struct.pack(
        "10s 10s i s 15s f",
        first_name.encode(),
        last_name.encode(),
        age,
        gender.encode(),
        occupstion.encode(),
        weight,
    )

    host = socket.gethostname()  # "localhost"
    port = 5000  # 8888  # 5000

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    #  client.sendall(b"Hello, world")
    for _ in range(100):
        client.send(data)
        time.sleep(1)
    client.close()


if __name__ == "__main__":
    main()



# cd "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste Socket Packaging Data Using Structs"
# python client.py
