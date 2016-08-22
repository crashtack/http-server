# -*- coding: utf-8 -*-
"""File contains a simple HTTP server."""
from __future__ import unicode_literals
import socket
import os
import io
from mimetypes import guess_type
try:
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPException

CRLF = '\r\n'
ROOT = './webroot'


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
            msg = response_error(exception)
        try:
            uri_data_tuple = resolve_uri(uri)
        except HTTPException as exception:
            msg = response_error(exception)
        try:
            msg = response_ok(uri_data_tuple)
        except HTTPException:
            msg = (response_error("500 Internal Server Error"))

        conn.sendall(msg.encode("utf-8"))
        conn.close()


def resolve_uri(uri):
    if uri.find('../') is not -1:
        raise HTTPException('404 File Not Found')
    elif uri[-1] == '/':
        return response_ok((generate_directory_html(uri), 'text/html'))
    else:
        try:
            file_data_tuple = get_file_data(uri)
        except HTTPException:
            raise HTTPException('404 File Not Found')
        return file_data_tuple


def get_file_data(uri):
    '''Reads file and returns a tuple: (file_dat, content-type).'''
    try:
        file_b = io.open(uri, 'rb')
    except IOError:
        raise HTTPException('404 File Not Found')
    mimetype = guess_type(uri)[0]
    binary_file = file_b.read()
    file_b.close
    unicode_file = binary_file.encode('utf8')
    return (unicode_file, mimetype)


def generate_directory_html(directory):
    """Generate an HTML string showing the contents of a directory.

    os.listdir and ignoring hidden files function from:
    from: http://stackoverflow.com/questions/7099290/how-to-ignore-hidden-
    files-using-os-listdir-python
    """
    try:
        file_list = []
        for f in os.listdir(ROOT + directory):
            if not f.startswith('.') and f is not None:
                file_list.append(f)
        print('file list', file_list)
        file_list.sort()
    except ValueError:
        # need to do something else here
        return HTTPException("404 File Not Found")
    except FileNotFoundError:
        """FileNotFoundError seems to be an OSX thing, and this line catches it
        despite the linter being very unhappy."""
        return HTTPException("404 File Not Found")
    out_string = '<html>\n\t<body>\n\t\t<ul>\n'
    for f in file_list:
        last_file = len(file_list) - 1
        if f == file_list[last_file]:
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
    try:
        body_len = len(body_tuple[0].encode('utf8'))
    except AttributeError:
        body_len = len(body_tuple[0])

    response = ('HTTP/1.1 200 OK\r\n'
                'Host: 127.0.0.1:5000\r\n'
                'Content-Type: {0}\r\n'
                'Content-Length: {1}\r\n\r\n'
                '{2}')
    response = response.format(body_tuple[1], body_len, body_tuple[0])
    return response


def response_error(code_and_reason):
    """Return a formatted http error response using the code received."""
    body = ("<html>\n<head>\n\t<title>{}</title>\n"
            "</head>\n<body>\n\t<h1>{}</h1>\n</body>\n</html>")
    body = body.format(code_and_reason, code_and_reason)
    body_len = len(body.encode('utf8'))
    response = ("HTTP/1.1 {}\r\nHost: 127.0.0.1:5000\r\n"
                "Content-Type: text/html\r\nContent-Length: {}\r\n\r\n{}")
    response = response.format(code_and_reason, body_len, body)
    return response


if __name__ == '__main__':
    server()
