# -*- coding: utf-8 -*-
"""Summary.

test needed.

1. messages shorter than 1 buffer length
2. message longer than several buffer lengths
3. messages that are multiples of 1 buffer length
4. messages containing non-ascii chars
"""
import pytest

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
    ("´©˙π", "´©˙π")
]


def test_set_up():
    """Set up server for testing purposes."""
    from server import server
    server()


def test_tear_down():
    """Tear down testing server."""
    from server import server
    server.shutdown(1)
    server.close()


@pytest.mark.parametrize('input, output', TEST_SHORT_BUFFERS)
def test_short_buffers(input, output):
    """Summary.

    Returns:
        TYPE: Description
    """
    from client import client
    test_set_up()
    assert client(input) == output
    test_tear_down()


@pytest.mark.parametrize('input, output', TEST_LONG_BUFFERS)
def test_long_buffers(input, output):
    """Summary.

    Returns:
        TYPE: Description
    """
    from client import client
    test_set_up()
    assert client(input) == output
    test_tear_down()


@pytest.mark.parametrize('input, output', TEST_BUFFER_MULTIPLES)
def test_buffer_multiples(input, output):
    """Summary.

    Returns:
        TYPE: Description
    """
    from client import client
    test_set_up()
    assert client(input) == output
    test_tear_down()


@pytest.mark.parametrize('input, output', TEST_NON_ASCII)
def test_non_ascii(input, output):
    """Summary.

    Returns:
        TYPE: Description
    """
    from client import client
    test_set_up()
    assert client(input) == output
    test_tear_down()
