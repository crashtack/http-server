# -*- coding: utf-8 -*-
"""Test file performs tests on client.py and server.py."""
from __future__ import unicode_literals
from server import response_ok
import pytest
try:
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPException

CRLF = '\r\n'


@pytest.fixture
def invalid_request():
    request = (b"GET /favicon.ico HTTP/1.1\r\n"
               b"Host: 127.0.0.1:5000\r\n"
               b"Connection: keep-alive\r\n"
               b"Accept-Language: en-US,en;q=0.8"
               b"This is a sample message body!")
    return request


@pytest.fixture
def valid_request():
    request = (b"GET /favicon.ico HTTP/1.1\r\n"
               b"Host: 127.0.0.1:5000\r\n"
               b"Connection: keep-alive\r\n"
               b"Accept-Language: en-US,en;q=0.8\r\n\r\n"
               b"This is a sample message body!")
    return request


def test_parse_request(request):
    """Function splits server request into test-able pieces."""
    from server import parse_request
    request = request.decode('utf-8')
    headers, body = request.split(CRLF + CRLF, 1)
    header_lines = headers.split(CRLF)
    return header_lines, body


def test_parse_request_no_CLRFCLRF(invalid_request):
    """tests check for no CLRF + CLRF"""
    from server import parse_request
    with pytest.raises(HTTPException):
            parse_request(invalid_request)


def test_parse_request_valid_GET_HTTP11(valid_request):
    """tests that parse_request returns the requested path of
       a valid GET path HTTP/1.1 request
       """
    from server import parse_request
    assert parse_request(valid_request) == u'/favicon.ico'


def test_parse_request_valid_GET_HTTP10():
    """tests that parse_request returns the requested path of
       a valid GET path HTTP/1.1 request
       """
    from server import parse_request
    test_header = (b"GET /favicon.ico HTTP/1.0\r\nHost: 127.0.0.1:5000\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException):
        parse_request(test_header)


def test_response_ok_one():
    """Test response_ok with specific test data."""
    temp = response_ok()
    assert isinstance(temp, bytes)


def test_response_ok_two():
    """Test response_ok with specific test data."""
    temp = response_ok()
    header_lines, body = response_ok(temp)
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
    # temp = response_error()
    header_lines, body = response_error()
    temp2 = header_lines[0].split()
    assert temp2[0] == 'HTTP/1.1'
    assert temp2[1] == '500'
    assert temp2[2] == 'Internal'
    assert temp2[3] == 'Server'
    assert temp2[4] == 'Error'
