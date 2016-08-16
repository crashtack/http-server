# -*- coding: utf-8 -*-
"""Summary."""
from __future__ import unicode_literals
import socket


def server():
    """Summary.

    Returns:
        TYPE: Description
    """
    while True:
        server = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM,
                               socket.IPPROTO_TCP)
        address = ('127.0.0.1', 5002)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(address)

        server.listen(1)
        conn, addr = server.accept()

        message = ""
        buffer_length = 8
        message_complete = False
        while not message_complete:
            part = conn.recv(buffer_length)
            # print('part: {}'.format(part))
            try:
                message += (part.decode('utf8'))
            except UnicodeDecodeError:
                message = 'utf8 decode error'
                message_complete = True
                break
            if len(part) < buffer_length:
                # print(message)
                message_complete = True
        conn.sendall(message.encode('utf8'))
        conn.close()


if __name__ == '__main__':
    server()
