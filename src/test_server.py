# -*- coding: utf-8 -*-
"""Test file performs tests on client.py and server.py."""
from server import response_ok


def test_response_ok_one():
    """Test response_ok with specific test data."""
    temp = response_ok()
    assert isinstance(temp, bytes)


def test_response_ok_two():
    """Test response_ok with specific test data."""
    temp = response_ok().split()
    assert temp[0] == b"HTTP/1.1"
    assert temp[1] == b"200"
    assert temp[2] == b"OK"


def test_response_error_one():
    """Test response_ok with specific test data."""
    from server import response_error
    temp = response_error()
    assert isinstance(temp, bytes)


def test_response_error_two():
    """Test response_error with test data."""
    from server import response_error
    temp = response_error().split()
    assert temp[0] == b'HTTP/1.1'
    assert temp[1] == b'500'
    assert temp[2] == b'Internal'
    assert temp[3] == b'Server'
    assert temp[4] == b'Error'
