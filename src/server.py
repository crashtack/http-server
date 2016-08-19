# -*- coding: utf-8 -*-
"""This file contains a simple HTTP echo server."""
from __future__ import unicode_literals
import socket

CRLF = '\r\n'


def server():
    """Function is a simple HTTP Echo server."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(1)
    buffer_length = 8

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
    response = (b"HTTP/1.1 200 OK\r\n"
                b"Host: 127.0.0.1:5000\r\n\r\n"
                b"Connection Successful")
    return response


def response_error():
    """Function returns an HTTP '500 Internal Server Error' response."""
    response = (b"HTTP/1.1 500 Internal Server Error\r\n"
                b"Host: 127.0.0.1:5000\r\n\r\n"
                b"Server Error")
    return response


def split_response(msg):

    msg = msg.decode('utf-8')
    try:
        head, body = msg.split(CRLF + CRLF, 1)
    except ValueError:
        return False


def parse_message(msg):
    """Function splits a server message into a head and a body"""
    msg = msg.decode('utf-8')
    try:
        head, body = msg.split(CRLF + CRLF, 1)
    except ValueError:
        return 'ValueError'
    header_lines = head.split(CRLF)
    first_line = header_lines[0]
    print('first_line: {}'.format(first_line))
    return header_lines, body


if __name__ == '__main__':
    server()
