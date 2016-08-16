# -*- coding: utf-8 -*-
"""Summary."""
import socket


def client():
    """Summary.

    Returns:
        TYPE: Description
    """
    infos = socket.getaddrinfo('127.0.0.1', 5002)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]

    echo_client = socket.socket(*stream_info[:3])
    echo_client.connect(stream_info[-1])

    message = u'Hello over there in the other window'
    echo_client.sendall(message.encode('utf8'))

    # echo_client.listen(2)
    # conn, addr = echo_client.accept()

    message = ""
    buffer_length = 8
    return_message_complete = False
    while not return_message_complete:
        part = echo_client.recv(buffer_length)
        message += (part.decode('utf8'))
        if len(part) < buffer_length:
            print(str(message))
            print("I like boats")
            # conn.sendall(message.encode('utf8'))
            echo_client.close()
            return_message_complete = True

if __name__ == '__main__':
    client()
