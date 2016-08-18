# -*- coding: utf-8 -*-
"""Test file performs tests on client.py and server.py."""
from __future__ import unicode_literals
from server import response_ok

CRLF = '\r\n'


def parse_request(request):
    """Function splits server request into test-able pieces."""
    request = request.decode('utf-8')
    headers, body = request.split(CRLF + CRLF, 1)
    header_lines = headers.split(CRLF)
    return header_lines, body


def test_parse_request():
    """Function tests that parse_request is processing responses correctly.

    The header I'm using here for testing is (mostly) an actual request
    header copied over from Chrome.
    """
    test_header = (b"GET /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n"
    b"Connection: keep-alive\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac "
    b"OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) "
    b"Chrome/52.0.2743.116 Safari/537.36\r\nAccept: */*\r\nReferer: "
    b"http://127.0.0.1:5000/\r\nAccept-Encoding: gzip, deflate, sdch\r\n"
    b"Accept-Language: en-US,en;q=0.8\r\n\r\nThis is a sample message body!")
    header_lines, body = parse_request(test_header)
    assert isinstance(header_lines[0], str)
    for line in header_lines:
        assert CRLF + CRLF not in line


def test_response_ok_one():
    """Test response_ok with specific test data."""
    temp = response_ok()
    assert isinstance(temp, bytes)


def test_response_ok_two():
    """Test response_ok with specific test data."""
    temp = response_ok()
    header_lines, body = parse_request(temp)
    temp2 = header_lines[0].split()
    assert temp2[0] == "HTTP/1.1"
    assert temp2[1] == "200"
    assert temp2[2] == "OK"


def test_response_error_one():
    """Test response_ok with specific test data."""
    from server import response_error
    temp = response_error()
    assert isinstance(temp, bytes)


def test_response_error_two():
    """Test response_error with test data."""
    from server import response_error
    temp = response_error()
    header_lines, body = parse_request(temp)
    temp2 = header_lines[0].split()
    assert temp2[0] == 'HTTP/1.1'
    assert temp2[1] == '500'
    assert temp2[2] == 'Internal'
    assert temp2[3] == 'Server'
    assert temp2[4] == 'Error'
