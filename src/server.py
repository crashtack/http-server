# -*- coding: utf-8 -*-
"""This file contains a simple HTTP echo server."""
from __future__ import unicode_literals
import socket
import os
import io
try:
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPException

CRLF = '\r\n'
ROOT = './webroot/'


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
            uri = parse_request(message)
        except HTTPException as exception:
            msg = (response_error(exception).encode("utf-8"))

        try:
            uri_data_tuple = resolve_uri(uri)
        except HTTPException as exception:
            msg = (response_error(exception).encode("utf-8"))
        # response_ok should return a byte string
        msg = response_ok(uri_data_tuple)
        try:
            conn.sendall(msg)
        except:
            pass

        conn.send()
        conn.close()


def resolve_uri(uri):
    if uri.find('../') is not -1:
        raise HTTPException('404 File Not Found')
    elif uri[-1] == '/':
        # response_ok should return a byte string
        return response_ok((generate_ls_html(uri), 'text/html'))
    else:
        try:
            file_data_tuple = get_file_date(uri)
        except HTTPException:
            raise HTTPException('404 File Not Found')
        return file_data_tuple


def get_file_date(uri):
    '''returns a tuple (file_dat, content-type)'''
    if uri.rsplit('.', maxsplit=1)[-1] == 'html':
        try:
            f = io.open(uri, encoding='utf-8')
        except FileNotFound:
            raise HTTPException('404 File Not Found')
        html_file = f.read()
        f.close
        return (html_file, 'text/html')
    pass


def generate_ls_html(directory):
    '''generate an HTML string showing the contents of a directory'''
    try:
        files = os.listdir(ROOT + directory)
        files.sort()
    except ValueError:
        # need to do something else here
        print("that didn't work")
    out_string = '<http>\n\t<body>\n\t\t<ul>\n'
    for f in files:
        last_file = len(files) - 1
        if f == files[last_file]:
            out_string += '\t\t\t<li>{}</li>\n\t\t</ul>\n\t</body>\n</html>'\
                          .format(f)
        else:
            out_string += '\t\t\t<li>{}</li>\n'.format(f)
    return out_string


def parse_request(request):
    """Parse incoming http request for errors and return uri."""
    request2 = request.decode('utf8')
    split_msg = request2.split(CRLF + CRLF, 1)
    head = split_msg[0]
    head_lines = head.split(CRLF)
    first_line = head_lines.pop(0)
    try:
        method, uri, proto = first_line.split()
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
        return uri


def response_ok(body_tuple):
    """Return a formatted HTTP '200 OK' response."""
    # I think body needs to be a byte string when it comes in
    # but byte strings do not have a .format Method
    # so i'm currently passing it in as a unicode string
    body_len = len(body_tuple[0].encode('utf8'))

    response = (u'HTTP/1.1 200 OK\r\n'
                u'Host: 127.0.0.1:5000\r\n'
                u'Content-Type: {}\r\n'
                u'Content-Length: {}\r\n\r\n'
                u'{}')
    response = response.format(body_tuple[1], body_len, body_tuple[0])
    # print('response_ok:\n{}'.format(response))
    return response


def response_error(code_and_reason):
    """Return an http response based on code received."""
    body = (u'<html>\n<head>\n'
            u'\t<title>{}</title>\n'
            u'</head>\n<body>\n'
            u'\t<h1>{}</h1>\n'
            u'</body>')
    body = body.format(code_and_reason, code_and_reason)
    body_len = len(body.encode('utf8'))
    response = (u'HTTP/1.1 {}\r\n'
                u'Host: 127.0.0.1:5000\r\n'
                u'Content-Type: text/html\r\n'
                u'Content-Length: {}\r\n\r\n'
                u'{}')
    response = response.format(code_and_reason, body_len, body)
    return response


if __name__ == '__main__':
    server()
