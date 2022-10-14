import socket
import threading

# https://www.youtube.com/watch?v=3UOyky9sEQY
# https://www.neuralnine.com/tcp-chat-in-python/


def main():

    host = "127.0.0.1"  # "localhost"
    port = 5000  # 55555

    # Choosing Nickname
    nickname = input("Choose your nickname: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))

        # Listening to Server and Sending Nickname
        def receive():
            while True:
                try:
                    # Receive Message From Server
                    # If 'NICK' Send Nickname
                    message = client.recv(1024).decode()  # "ascii"
                    if message == "NICK":
                        client.send(nickname.encode())  # "ascii"
                    else:
                        print(message)
                except:
                    # Close Connection When Error
                    print("An error occured!")
                    client.close()
                    break

        # Sending Messages To Server
        def write():
            while True:
                message = "{}: {}".format(nickname, input(""))
                client.send(message.encode())  # "ascii"

        # Starting Threads For Listening And Writing
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        write_thread = threading.Thread(target=write)
        write_thread.start()


if __name__ == "__main__":
    main()


# cd "C:\Users\chris\Desktop\CMS Python\CMS Teste API e Web\CMS Teste Socket Simple TCP Chat Room"
# python client.py
