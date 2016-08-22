# -*- coding: utf-8 -*-
"""Test file performs tests on client.py and server.py."""
from __future__ import unicode_literals
import pytest
try:
    from http.client import HTTPException
except ImportError:
    from httplib import HTTPException
from conftest import LS_TABLE
from conftest import BAD_RESPONSE_TABLE
from conftest import GOOD_RESPONSE_TABLE
from conftest import FILE_DATA_TABLE

CRLF = '\r\n'


# --------------------------------------------------------------------
# Start resolve_uri tests
# --------------------------------------------------------------------

def test_resolve_uri_import():
    """from server import resolve_uri
    test for 2 errors plus successful output"""
    pass


# --------------------------------------------------------------------
# Start generate_directory tests
# --------------------------------------------------------------------
@pytest.mark.parametrize('uri, result', LS_TABLE)
def test_generate_directory_html(uri, result):
    from server import generate_directory_html
    output = generate_directory_html(uri)
    # print('output: {}'.format(output))
    assert output == result


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


def test_parse_request_empty_first_line():
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
    """Test that parse_request returns HTTPException for PUT method."""
    from server import parse_request
    test_header = (b"PUT /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:5000\r\n"
                   b"Connection: keep-alive\r\n"
                   b"Accept-Language: en-US,en;q=0.8\r\n\r\n"
                   b"This is a sample message body!")
    with pytest.raises(HTTPException) as excinfo:
        parse_request(test_header)
    assert '405 Method Not Allowed' in str(excinfo)


def test_parse_request_no_host():
    """Test that parse_request throws 400 error when HOST line in request."""
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
@pytest.mark.parametrize('uri, result', FILE_DATA_TABLE)
def tests_get_file_data(uri, result):
    '''tests that get_file_data returns proper file tuple'''
    from server import get_file_data
    with pytest.raises(HTTPException) as excinfo:
        get_file_data(uri)
    assert '404 File Not Found' in str(excinfo)


@pytest.mark.parametrize('directory, body_type, result', GOOD_RESPONSE_TABLE)
def test_response_ok(directory, body_type, result):
    """Test response_ok with specific test data."""
    from server import response_ok
    from server import generate_directory_html as gen_dir_html
    assert response_ok((gen_dir_html(directory), body_type)) == result


@pytest.mark.parametrize('error, result', BAD_RESPONSE_TABLE)
def test_response_error(error, result):
    """Test response_error with supplied error code."""
    from server import response_error
    compare = response_error(error)
    print('this is the generated error', compare)
    print('this is the expected result', result)
    assert compare.strip() == result.strip()
