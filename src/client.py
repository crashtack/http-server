# -*- coding: utf-8 -*-
"""File contains a simple HTTP echo client."""
from __future__ import unicode_literals
import socket
import sys


def client_send(msg):
    """Function contains a simple HTTP echo client."""
    infos = socket.getaddrinfo('127.0.0.1', 5002)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])

    try:   # this try/except block is here for python 2.7
        msg = msg.decode('utf8')
    except AttributeError:  # in Python 3 unicode do not have a .decode method
        pass

    encoded_message = msg.encode('utf8')

    client.sendall(encoded_message)
    client.shutdown(socket.SHUT_WR)

    echoed_message = b''
    buffer_length = 8
    return_message_complete = False
    while not return_message_complete:
        part = client.recv(buffer_length)
        echoed_message += part
        if len(part) < buffer_length:
            return_message_complete = True
    client.close()
    return echoed_message.decode('utf8')

if __name__ == '__main__':
    print(client_send(sys.argv[1]))
