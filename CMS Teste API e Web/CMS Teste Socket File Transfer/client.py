import os
import pathlib
import socket

from tqdm import tqdm


def main():

    BUFFER_SIZE = 4096  # 1024
    SEPARATOR = "<SEPARATOR>"

    filename = pathlib.Path(__file__).parent.joinpath("img_client.jpg")
    file_size = os.path.getsize(filename=filename)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(("localhost", 5000))

        # client.send("img_server.jpg".encode())
        # client.send(str(file_size).encode())
        # client.sendall(data)

        client.send(f"img_server.jpg{SEPARATOR}{file_size}".encode())

        progress = tqdm(
            range(int(file_size)),
            f"Sending img_client.jpg",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

        with open(file=filename, mode="rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                client.sendall(bytes_read)
                progress.update(len(bytes_read))

        # client.send(b"<END>")


if __name__ == "__main__":
    main()


# cd "C:\Users\chris\Desktop\CMS Python\CMS Teste API e Web\CMS Teste Socket File Transfer"
# python client.py
