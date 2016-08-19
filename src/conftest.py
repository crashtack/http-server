# -*- coding: utf-8 -*-
import pytest

CRLF = '\r\n'


@pytest.fixture
def valid_200_response():
    response = (b'HTTP/1.0 200 OK\r\n'
                b'Date: Fri, 31 Dec 1999 23:59:59 GMT\r\n'
                b'Content-Type: text/html\r\n'
                b'Transfer-Encoding: chunked\r\n\r\n'
                b'This is the content!!!!!!!!!!!!!!\r\n'
                b'blalbblbl poopsauce\r\n\r\n')
    return response


@pytest.fixture
def parse_request(request):
    """Function splits a server request into a head and a body"""
    request = request.decode('utf-8')
    headers, body = request.split(CRLF + CRLF, 1)
    header_lines = headers.split(CRLF)
    return header_lines, body


def split_response(response):
    pass

    # status_line     # request for request, status for response
    # header_lines
    # measage_body
