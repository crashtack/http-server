# -*- coding: utf-8 -*-
"""Test file performs tests on client.py and server.py."""
from __future__ import unicode_literals
from server import response_ok, response_error, parse_message

CRLF = '\r\n'


def test_parse_message_good(valid_200_response):
    """Testing parse_message with a valid_200_response"""
    header_lines, body = parse_message(valid_200_response)
    print('header lines: {}'.format(header_lines))
    print('body: {}'.format(body))
    assert 1 == 1

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
