# -*- coding: utf-8 -*-
import pytest

CRLF = '\r\n'

LS_TABLE = [
    ('/',
     ('<http>\n\t<body>\n\t\t<ul>\n'
      '\t\t\t<li>a_web_page.html</li>\n'
      '\t\t\t<li>images</li>\n'
      '\t\t\t<li>make_time.py</li>\n'
      '\t\t\t<li>sample.txt</li>\n'
      '\t\t</ul>\n\t</body>\n</html>')),
    ('/images/',
     ('<http>\n\t<body>\n\t\t<ul>\n'
      '\t\t\t<li>JPEG_example.jpg</li>\n'
      '\t\t\t<li>Sample_Scene_Balls.jpg</li>\n'
      '\t\t\t<li>sample_1.png</li>\n'
      '\t\t</ul>\n\t</body>\n</html>')),
]

BAD_RESPONSE_TABLE = [
    ('400 Bad Request',
     ('HTTP/1.1 400 Bad Request\r\n'
      'Host: 127.0.0.1:5000\r\n'
      'Content-Type: text/html\r\n'
      'Content-Length: 94\r\n\r\n'
      '<html>\n'
      '<head>\n'
      '\t<title>400 Bad Request</title>\n'
      '</head>\n'
      '<body>\n'
      '\t<h1>400 Bad Request</h1>\n'
      '</body>')),
]


# adapted from http://pytest.org/latest/example/special.html
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
                b'blalbblbl poopsauce\r\n\r\n')
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
