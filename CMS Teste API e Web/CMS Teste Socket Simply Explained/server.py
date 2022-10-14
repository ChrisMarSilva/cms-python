import socket
import threading


def simply_server():
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


def thread_server():

    HEADER = 64
    FORMAT = "utf-8"
    DISCONNECT_MESSAGE = "!DISCONNECT"
    SERVER = socket.gethostbyname(socket.gethostname())
    PORT = 5000
    ADDR = (SERVER, PORT)

    def handle_client(conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg}")
                conn.send("Msg received".encode(FORMAT))
        conn.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(ADDR)
        print("[STARTING] server is starting...")
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def main():
    # simply_server()
    thread_server()


if __name__ == "__main__":
    main()


# cd "C:\Users\chris\Desktop\CMS Python\CMS Teste API e Web\CMS Teste Socket Simply Explained"
# python server.py
