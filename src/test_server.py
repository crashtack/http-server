# -*- coding: utf-8 -*-
"""Test file performs tests on client.py and server.py."""
from __future__ import unicode_literals
from server import response_ok, response_error, parse_message
import pytest
try:
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPException

CRLF = '\r\n'


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
    assert excinfo.args[0] == '400 Bad Request'


def test_parse_request_valid_get_http11(valid_get):
    """Test that parse_request returns a valid GET path HTTP/1.1 request."""
    from server import parse_request
    assert parse_request(valid_get) == u'/path/file.html'


def test_parse_request_bad_headline():
    """Test that parse_request returns HTTPException bad headline"""
    from server import parse_request
    test_header = (b"GETTTP/1.1\r\n"
                   b"Host: 127.0.0.1:5000\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n\r\n"
                   b"This is a sample message body!")
    with pytest.raises(ValueError) as excinfo:
        parse_request(test_header)
    assert '400 Bad Request' in str(excinfo)


def test_parse_request_http10():
    """Test that parse_request returns HTTPException for HTTP/1.0."""
    from server import parse_request
    test_header = (b"GET /favicon.ico HTTP/1.0\r\nHost: 127.0.0.1:5000\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException) as (excinfo):
        parse_request(test_header)
    assert '505 HTTP Version Not Supported' in str(excinfo)


def test_parse_request_put():
    """Test that parse_request returns HTTPException for HTTP/1.0."""
    from server import parse_request
    test_header = (b"PUT /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException) as (excinfo):
        parse_request(test_header)
    assert '405 Method Not Allowed' in str(excinfo)


def test_parse_request_no_host(invalid_request):
    """tests check for no CLRF + CLRF"""
    from server import parse_request
    test_header = (b"GETTTP/1.1\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException) as (excinfo):
        parse_request(test_header)
    assert '400 Bad Request' in str(excinfo)

# --------------------------------------------------------------------
# End parse_message tests
# --------------------------------------------------------------------


def test_parse_message_good(valid_200_response):
    """Testing parse_message with a valid_200_response"""
    header_lines, body = parse_message(valid_200_response)
    print('header lines: {}'.format(header_lines))
    print('body: {}'.format(body))
    assert 1 == 1


def test_parse_message_bad(valid_200_response):
    """Testing parse_message with a valid_200_response"""
    with pytest.raises(IndexError):
        parse_message(b'poops    hufyu   vfyauce')


def test_response_ok_is_bytes():
    """Test response_ok with specific test data."""
    temp = response_ok()
    assert isinstance(temp, bytes)


def test_response_ok_two():
    """Test response_ok with specific test data."""
    temp = response_ok()
    header_lines, body = parse_message(temp)
    temp2 = header_lines[0].split()
    assert temp2[0] == "HTTP/1.1"
    assert temp2[1] == "200"
    assert temp2[2] == "OK"


def test_response_error_one():
    """Test response_ok with specific test data."""
    from server import response_error
    temp = response_error()
    assert isinstance(temp, bytes)


def test_response_error_proto():
    temp = response_error()
    header_lines, body = parse_message(temp)
    firsts_line = header_lines[0].split()
    proto = firsts_line[0]
    assert proto == 'HTTP/1.1'


def test_response_error_code():
    temp = response_error()
    header_lines, body = parse_message(temp)
    firsts_line = header_lines[0].split()
    code = firsts_line[1]
    assert code == '500'


def test_response_error_reason():
    temp = response_error()
    header_lines, body = parse_message(temp)
    first_line = header_lines[0].split()
    reason = ''
    for word in first_line[2:]:
        reason += word + ' '
    assert reason == 'Internal Server Error '


def test_response_error_address():
    temp = response_error()
    header_lines, body = parse_message(temp)
    second_line = header_lines[1].split()
    line = ''
    for word in second_line[:]:
        print('word: {}'.format(word))
        line += word + ' '
    assert line == 'Host: 127.0.0.1:5000 '
