# -*- coding: utf-8 -*-
"""Summary."""
from __future__ import unicode_literals
import socket

# TODO: move the server creation lines out of while loop 16 - 23


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

        message = b''  # TODO: change to message = b""
        buffer_length = 8
        message_complete = False
        while not message_complete:
            part = conn.recv(buffer_length)
            # print('part: {}'.format(part))
            message += part

            if len(part) < buffer_length:
                # print(message)
                message_complete = True
        conn.sendall(message)
        conn.close()
        # close the server

if __name__ == '__main__':
    server()
