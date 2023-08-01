import socket

from threading import Thread

HOST = "127.0.0.1"
PORT = 12345


def send_msg(s: socket.socket, username: str) -> None:
    try:
        while True:
            message = input()
            if message == "/exit":
                s.sendall(f"User {username} has left the chat".encode())
                s.close()
                break
            chat_msg = f"{username}: {message}"
            s.sendall(chat_msg.encode())
    except ConnectionError as e:
        print(e)


def get_msg(s: socket.socket) -> None:
    try:
        while True:
            data = s.recv(1024)
            if not data:
                break
            print(f"{data.decode()}")
    except ConnectionError as e:
        print(e)


def chat(s:socket.socket, username: str) -> None:
    get_msg(s)
    send_msg(s, username)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    username = input("Your name: ")
    print(f'Welcome to chat, {username}!\n"/exit" - leave the chat')

    thr1 = Thread(target=chat, args=(s, username))
    thr1.start()
    thr1.join()
