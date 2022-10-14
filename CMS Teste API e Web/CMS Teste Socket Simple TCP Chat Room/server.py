import socket


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 5000))
        server.listen(5)

        while True:
            conn, addr = server.accept()
            print(f"Connected to {addr}")

            if conn:
                data = conn.recv(1024)
                if not data:
                    break
                if len(str(data)) <= 0:
                    break

                print(data.decode("utf-8"))

                data = "Got yout message! Thank you!"
                conn.send(data.encode("utf-8"))


if __name__ == "__main__":
    main()


# cd "C:\Users\chris\Desktop\CMS Python\CMS Teste API e Web\CMS Teste Socket Simple TCP Chat Room"
# python server.py
