import socket

from threading import Thread

HOST = "127.0.0.1"
PORT = 12345


def send_msg(s: socket.socket, username: str) -> None:
    while True:
        message = input()
        if message == "/exit":
            s.sendall(f"User {username} has left".encode())
            s.close()
            break
        chat_msg = f"{username}: {message}"
        s.sendall(chat_msg.encode())


def get_msg(s: socket.socket) -> None:
    while True:
        data = s.recv(1024)
        if not data:
            break
        print(f"{data.decode()}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    username = input("Your name: ")
    print(f'Welcome to chat, {username}!\n"/exit" - leave the chat')

    thr1 = Thread(target=send_msg, args=(s, username))
    thr2 = Thread(target=get_msg, args=(s,))

    thr1.start()
    thr2.start()

    thr1.join()
    thr2.join()
