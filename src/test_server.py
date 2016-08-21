# -*- coding: utf-8 -*-
"""Test file performs tests on client.py and server.py."""
from __future__ import unicode_literals
import pytest
try:
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPException

CRLF = '\r\n'


# --------------------------------------------------------------------
# Start resolve_uri tests
# --------------------------------------------------------------------

def test_resolve_uri_import():
    from server import resolve_uri


# --------------------------------------------------------------------
# End resolve_uri tests
# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Start parse_message tests
# --------------------------------------------------------------------


def test_parse_request_no_clrfclrf(invalid_request):
    """Test checks for no CLRF + CLRF."""
    from server import parse_request
    test_header = (b"GETTTP/1.1\r\n"
                   b"Host: 127.0.0.1:5000\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException) as excinfo:
        parse_request(test_header)
    assert '400 Bad Request' in str(excinfo)


def test_parse_request_valid_get_http11(valid_get):
    """Test that parse_request returns a valid GET path HTTP/1.1 request."""
    from server import parse_request
    assert parse_request(valid_get) == u'/path/file.html'


def test_parse_request_bad_first_line():
    """Test that parse_request returns exception for bad first line."""
    from server import parse_request
    test_header = (b"GETTTP/1.1\r\n"
                   b"Host: 127.0.0.1:5000\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException) as excinfo:
        parse_request(test_header)
    assert '400 Bad Request' in str(excinfo)


def test_parse_requset_bad_first_line_two():
    """Test for handling an empty first line in the http request."""
    from server import parse_request
    test_header = (b"\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException) as errinfo:
        parse_request(test_header)
    assert "400 Bad Request" in str(errinfo)


def test_parse_request_http10():
    """Test that parse_request returns HTTPException for HTTP/1.0."""
    from server import parse_request
    test_header = (b"GET /favicon.ico HTTP/1.0\r\nHost: 127.0.0.1:5000\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException) as excinfo:
        parse_request(test_header)
    assert '505 HTTP Version Not Supported' in str(excinfo)


def test_parse_request_put():
    """Test that parse_request returns HTTPException for HTTP/1.0."""
    from server import parse_request
    test_header = (b"PUT /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException) as excinfo:
        parse_request(test_header)
    assert '405 Method Not Allowed' in str(excinfo)


def test_parse_request_no_host(invalid_request):
    """tests check for no CLRF + CLRF"""
    from server import parse_request
    test_header = (b"GET /favicon.ico HTTP/1.1\r\n"
                   b"Taco: 127.0.0.1:5000\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException) as excinfo:
        parse_request(test_header)
    assert '400 Bad Request' in str(excinfo)


# --------------------------------------------------------------------
# End parse_message tests
# --------------------------------------------------------------------


def test_response_ok_is_bytes():
    """Test response_ok with specific test data."""
    from server import response_ok
    temp = response_ok()
    assert isinstance(temp, bytes)


def test_response_error_one():
    """Test response_ok with specific test data."""
    from server import response_error
    temp = response_error("400 Bad Request")
    assert temp == ("HTTP/1.1 400 Bad Request\r\n"
                    "Host: 127.0.0.1:5000\r\n\r\n"
                    "400 Bad Request")
