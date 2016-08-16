# -*- coding: utf-8 -*-
"""Summary.

test needed.

1. messages shorter than 1 buffer length
2. message longer than several buffer lengths
3. messages that are multiples of 1 buffer length
4. messages containing non-ascii chars
"""
import pytest
from client import client_send

TEST_SHORT_BUFFERS = [
    ("1234", "1234"),
    ("string", "string"),
    ("13 Elms", "13 Elms")
]
TEST_LONG_BUFFERS = [
    ("thisisalongstring", "thisisalongstring"),
    ("thisisalongerstringwoooo", "thisisalongerstringwoooo")
]
TEST_BUFFER_MULTIPLES = [
    ("12345678", "12345678"),
    ("1234567812345678", "1234567812345678")
]
TEST_NON_ASCII = [
    ("çç√√", "çç√√"),
    # ("çç√√", 'utf8 decode error'),
    ("´©˙π", "´©˙π"),
]


@pytest.mark.parametrize('input, output', TEST_SHORT_BUFFERS)
def test_short_buffers(input, output):
    """Test client_send with short test data."""
    assert client_send(input) == output


@pytest.mark.parametrize('input, output', TEST_LONG_BUFFERS)
def test_long_buffers(input, output):
    """Test client_send with long test data."""
    assert client_send(input) == output


@pytest.mark.parametrize('input, output', TEST_BUFFER_MULTIPLES)
def test_buffer_multiples(input, output):
    """Test client_send with multiples of buffer length."""
    assert client_send(input) == output


@pytest.mark.parametrize('input, output', TEST_NON_ASCII)
def test_non_ascii(input, output):
    """Test client_send with non-ascii characters."""
    assert client_send(input) == output
