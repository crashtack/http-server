# -*- coding: utf-8 -*-
"""Summary."""
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

    client.sendall(msg.encode('utf8'))
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
