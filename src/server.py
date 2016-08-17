# -*- coding: utf-8 -*-
"""This file contains a simple HTTP echo server."""
from __future__ import unicode_literals
import socket


def server():
    """Function is a simple HTTP Echo server."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5002)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(1)
    buffer_length = 8

    """Instead of this while True:   echoing (we need parts of it) we
        need to do the following:

    - accumulate the incoming request to a variable
    - 'log' request by printing it to stdout (console?)
    - return a well-formed HTTP 200 response if the request merits it,
    - or return a 500 server errror if the request is bad
    """

    while True:
        conn, addr = server.accept()
        message = b''
        message_complete = False
        while not message_complete:
            part = conn.recv(buffer_length)
            message += part
            if len(part) < buffer_length:
                message_complete = True

        print(message)
        conn.send(response_ok())
        conn.close()


def response_ok():
    """Function returns an HTTP '200 OK' response."""
    response = b"HTTP/1.0 200 OK\r\n"
    return response


def response_error():
    """Function returns an HTTP '500 Internal Server Error' response."""
    response = b"HTTP/1.1 500 Internal Server Error"
    return response


if __name__ == '__main__':
    server()
