import socket

from datetime import datetime
from threading import Thread

HOST = "127.0.0.1"
PORT = 12345

users = []


def new_client(connection: socket.socket, addr: tuple) -> None:
    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            print(f"{current_time} - {addr} - {data.decode()}")
            for user in users:
                if user is not connection:
                    user.sendall(data)

    users.remove(connection)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Chat server has been started")

    while True:
        conn, addr = s.accept()
        current_time = datetime.now().time()
        print(f"{current_time} - User {addr} has joined")
        users.append(conn)

        thr = Thread(target=new_client, args=(conn, addr))
        thr.start()
