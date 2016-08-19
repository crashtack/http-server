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


def parse_request(request):
    # print('request: {}'.format(request))
    urequest = request.decode('utf8')
    head, body = urequest.split(CRLF + CRLF, 1)
    # print('head: {}'.format(head))
    head_lines = head.split(CRLF)
    # print('head_lines: {}'.format(head_lines))

    for l in head_lines:
        # print('l: {}'.format(l))
        try:
            method, path, proto = l.split()
        except IndexError:
            raise HTTPException(b'400 Bad Request')
        if proto != 'HTTP/1.1':
            raise HTTPException(b'505 HTTP Version Not Supported')
        if method == 'GET':
            if path.find('../'):
                raise HTTPException(b'403 Forbidden')
            else:
                return path
        else:
            raise HTTPException(b'405 Method Not Allowed')


# def decode(reqest):
#     # casts byte string responce to UNICODE
#     uresponse = response.decode('utf8')
#     # uresponse.split(CRLF)
#
#     head, body = uresponse.split(CRLF + CRLF, 1)    # '1' splits only once
#
#     head_lines = head.split(CRLF)
#
#     proto, status = head_lines[0].split(maxsplit=1)
#     headers = head_lines[1:]
#
#     headers_split = [header.split(':', 1) for header in headers]
#
#     headers_dict = {k.lower(): v.strip() for k, v headers in headers_split}
#
#
#
# assert 'content-length' in headers_dict
# assert int(headers_dict['content-length']) = len(body.encode('utf8'))


def response_ok():
    """Function returns an HTTP '200 OK' response."""
    response = (b"HTTP/1.1 200 OK\r\nHost: 127.0.0.1:5000"
                b"\r\n\r\nConnection Successful")
    return response


def response_error():
    """Function returns an HTTP '500 Internal Server Error' response."""
    response = (b"HTTP/1.1 500 Internal Server Error\r\n"
                b"Host: 127.0.0.1:5000\r\n\r\nServer Error")
    return response


if __name__ == '__main__':
    server()
