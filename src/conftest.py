# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import pytest
from server import get_file_data

BAD_URI_TABLE = [
    ('../*.py', '403 Forbidden'),
    ('this_file_does_not_exist.py',
     '404 File Not Found'),
]
GOOD_URI_TABLE = [
    ('/', ("HTTP/1.1 200 OK\r\n"
           "Host: 127.0.0.1:5000\r\n"
           "Content-Type: text/html\r\n"
           "Content-Length: 141\r\n\r\n"
           "<html>\n"
           "\t<body>\n"
           "\t\t<ul>\n"
           "\t\t\t<li>a_web_page.html</li>\n"
           "\t\t\t<li>images</li>\n"
           "\t\t\t<li>make_time.py</li>\n"
           "\t\t\t<li>sample.txt</li>\n"
           "\t\t</ul>\n"
           "\t</body>\n"
           "</html>")),
    ('sample.txt', get_file_data('sample.txt'))
]


@pytest.fixture(scope="module", autouse=True)
def tear_down():
    print("\nTEARDOWN after all tests")


@pytest.fixture(scope="module", autouse=True)
def set_up(request):
    print("\nSETUP before all tests")

    def tear_down2():
        print("\nTEARDOWN after all tests")
    request.addfinalizer(tear_down2)


@pytest.fixture(scope="function")
def valid_200_response():
    response = (b'HTTP/1.1 200 OK\r\n'
                b'Date: Fri, 31 Dec 1999 23:59:59 GMT\r\n'
                b'Content-Type: text/html\r\n'
                b'Transfer-Encoding: chunked\r\n\r\n'
                b'This is the content!!!!!!!!!!!!!!\r\n'
                b'blalbblbl steaksauce\r\n\r\n')
    return response


@pytest.fixture(scope="function")
def valid_get():
    request = (b'GET /path/file.html HTTP/1.1\r\n'
               b'Date: Fri, 31 Dec 1999 23:59:59 GMT\r\n'
               b'Content-Type: text/html\r\n'
               b'Host: www.host1.com:80\r\n\r\n')
    return request


@pytest.fixture
def invalid_request():
    request = (b"GET /favicon.ico HTTP/1.1\r\n"
               b"Host: 127.0.0.1:5000\r\n"
               b"Connection: keep-alive\r\n"
               b"Accept-Language: en-US,en;q=0.8"
               b"This is a sample message body!")
    return request
