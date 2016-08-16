# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
"""Summary."""
from __future__ import unicode_literals
import socket
import sys


def client_send(msg):
    """Summary.

    Returns:
        TYPE: Description
    """

    infos = socket.getaddrinfo('127.0.0.1', 5002)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]

    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])

    try:    # this try/except block is here for python 2.7
        encoded_message = msg.encode('utf8')
        decoded_message = encoded_message.decode('utf8')
    except UnicodeDecodeError:
        print(' inside decode block')
        return 'utf8 encode error'

    client.sendall(encoded_message)
    # client.sendall(msg.encode('utf8'))
    client.shutdown(1)

    message_2 = ""
    buffer_length = 8
    return_message_complete = False
    while not return_message_complete:
        part = client.recv(buffer_length)
        message_2 += part.decode('utf8')
        if len(part) < buffer_length:
            return_message_complete = True
    client.close()
    return message_2

if __name__ == '__main__':
    print(client_send(sys.argv[1]))
