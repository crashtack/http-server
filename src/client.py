# -*- coding: utf-8 -*-
import socket


def client():
    infos = socket.getsddrinfo('127.0.0.1', 5001)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]

    echo_client = socket.socket(*stream_info[:3])
    echo_client.connect(stream_info[-1])

    message = u'Hello over there in the other window'
    client.sendall(message.encode('utf8'))






if __name__ == '__main__':
    client()
