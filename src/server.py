# -*- coding: utf-8 -*-
"""This file contains a simple HTTP echo server."""
from __future__ import unicode_literals
import socket
try:
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPException

CRLF = '\r\n'


def server():
    """Simple HTTP server loop."""
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
        try:
            parse_request(message)
        except HTTPException as exception:
            conn.send((response_error(exception).encode("utf-8")))
            conn.close()
        else:
            conn.send(response_ok())
        conn.close()


def parse_request(request):
    """Parse incoming http request for errors and return uri."""
    request2 = request.decode('utf8')
    split_msg = request2.split(CRLF + CRLF, 1)
    head = split_msg[0]
    head_lines = head.split(CRLF)
    first_line = head_lines.pop(0)
    try:
        method, path, proto = first_line.split()
    except ValueError:
        raise HTTPException('400 Bad Request')
    if proto != 'HTTP/1.1':
        raise HTTPException('505 HTTP Version Not Supported')
    if method != 'GET':
        raise HTTPException('405 Method Not Allowed')
    temp_1 = [l.split(":", 1) for l in head_lines]
    header_dict = {k.lower(): v.strip() for k, v in temp_1}
    if 'host' not in header_dict:
        raise HTTPException('400 Bad Request')
    else:
        return path


def response_ok():
    """Return a formatted HTTP '200 OK' response."""
    response = (b"HTTP/1.1 200 OK\r\n"
                b"Host: 127.0.0.1:5000\r\n\r\n"
                b"Connection Successful")
    return response


def response_error(code_and_reason):
    """Return an http response based on code received."""
    response = ("HTTP/1.1 {}\r\n"
                "Host: 127.0.0.1:5000\r\n\r\n"
                "{}")
    return response.format(code_and_reason, code_and_reason)


if __name__ == '__main__':
    server()
