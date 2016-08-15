# -*- coding: utf-8 -*-
import socket


def server():
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5001)
    server.bind(address)
    server.listen(1)
    conn, addr = server.accept()

    buffer_length = 8
    message_complete = False
    while not message_complete:
        part = conn.recv(buffer_length)
        print(part.decode('utf8'))
        if len(part) < buffer_length:
            message_complete = True


if __name__ == '__main__':
    server()
