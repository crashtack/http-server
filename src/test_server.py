# -*- coding: utf-8 -*-
"""Test file performs tests on client.py and server.py."""
# import pytest
# from client import client_send
from server import response_ok
# from server import response_error


def test_response_ok_one():
    """Test response_ok with specific test data."""
    temp = response_ok()
    assert isinstance(temp, bytes)


def test_response_ok_two():
    """Test response_ok with specific test data."""
    temp = response_ok().split()
    assert temp[0] == b"HTTP/1.0"
    assert temp[1] == b"200"
    assert temp[2] == b"OK"


def test_response_error():
    """Test response_error with test data."""
