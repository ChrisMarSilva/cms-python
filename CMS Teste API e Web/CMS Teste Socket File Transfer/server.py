import os
import pathlib
import socket

from tqdm import tqdm


def main():
    BUFFER_SIZE = 4096  # 1024
    SEPARATOR = "<SEPARATOR>"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 5000))
        server.listen(5)

        client, addr = server.accept()
        print(f"Connected to {addr}")

        # file_name = client.recv(1024).decode()
        # print(f"{file_name=}")

        # file_size = client.recv(1024).decode()
        # print(f"{file_size=}")

        # done = False
        # file_bytes = b""
        # progress = tqdm(
        #     unit="B",
        #     unit_scale=True,
        #     unit_divisor=1024,
        #     total=int(file_size),
        # )

        # while not done:
        #     data = client.recv(1024)
        #     file_bytes += data
        #     progress.update(1024)
        #     if file_bytes[-5:] == b"<END>":
        #         done = True

        # filename = pathlib.Path(__file__).parent.joinpath(file_name)
        # with open(file=filename, mode="wb") as f:
        #     f.write(file_bytes)

        received = client.recv(BUFFER_SIZE).decode()
        file_name, file_size = received.split(SEPARATOR)

        # file_name = os.path.basename(file_name)
        filename = pathlib.Path(__file__).parent.joinpath(file_name)
        file_size = int(file_size)

        progress = tqdm(
            range(file_size),
            f"Receiving {file_name}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            total=int(file_size),
        )

        with open(file=filename, mode="wb") as f:
            while True:
                bytes_read = client.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))

        client.close()


if __name__ == "__main__":
    main()


# cd "C:\Users\chris\Desktop\CMS Python\CMS Teste API e Web\CMS Teste Socket File Transfer"
# python server.py
