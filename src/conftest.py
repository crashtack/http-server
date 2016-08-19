# -*- coding: utf-8 -*-
import pytest

CRLF = '\r\n'


# adapted from http://pytest.org/latest/example/special.html
def tear_down():
    print("\nTEARDOWN after all tests")


# # to start up a server and keep it running
# @pytest.yield_fixture(autouse=True)
# def start_server():
#     # start some server and keep it running
#     pass


@pytest.fixture(scope="session", autouse=True)
def set_up(request):
    print("\nSETUP before all tests")

    def tear_down2():
        print("\nTEARDOWN after all tests")
    request.addfinalizer(tear_down2)


@pytest.fixture(scope="session")
def valid_200_response():
    response = (b'HTTP/1.1 200 OK\r\n'
                b'Date: Fri, 31 Dec 1999 23:59:59 GMT\r\n'
                b'Content-Type: text/html\r\n'
                b'Transfer-Encoding: chunked\r\n\r\n'
                b'This is the content!!!!!!!!!!!!!!\r\n'
                b'blalbblbl poopsauce\r\n\r\n')
    return response


@pytest.fixture(scope="session")
def valid_get():
    request = (b'GET /path/file.html HTTP/1.1\r\n'
               b'Host: www.host1.com:80\r\n\r\n')
    return request
