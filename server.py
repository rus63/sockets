import socket

from datetime import datetime
from threading import Thread
import logging

console_out = logging.StreamHandler()

logging.basicConfig(
    handlers=(console_out,),
    format="[%(asctime)s | %(levelname)s]: %(message)s",
    datefmt="%m.%d.%Y %H:%M:%S",
    level=logging.INFO,
)

HOST = "127.0.0.1"
PORT = 12345

users = []


def new_client(connection: socket.socket, addr: tuple) -> None:
    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            logging.info(f'{data.decode()}')
            for user in users:
                if user is not connection:
                    user.sendall(data)

    users.remove(connection)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    logging.info("Chat server has been started")

    while True:
        conn, addr = s.accept()
        current_time = datetime.now().time()
        logging.info(f"{current_time} - User {addr} has joined")
        users.append(conn)

        thr = Thread(target=new_client, args=(conn, addr))
        thr.start()
