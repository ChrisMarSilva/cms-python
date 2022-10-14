import socket


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 5000))
        server.listen(5)

        while True:
            conn, addr = server.accept()
            print(f"Connected to {addr}")

            data = conn.recv(1024)
            if not data:
                break

            print(data.decode("utf-8"))

            data = "Got yout message! Thank you!"
            conn.send(data.encode("utf-8"))


if __name__ == "__main__":
    main()


# cd "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste Socket Simply Explained"
# python server.py
