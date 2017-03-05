# github.com/MagicStack/vmbench/blob/master/servers/asyncio_http_server.py
import uvloop
import asyncio
import httptools

# test code

class HttpRequest:
    __slots__ = ('_protocol', '_url', '_headers', '_version', '_keep_alive')

    def __init__(self, protocol, url, headers, version):
        self._protocol = protocol
        self._url = url
        self._headers = headers
        self._version = version
        self._keep_alive = False


class HttpResponse:
    __slots__ = ('_protocol', '_request', '_headers_sent')

    def __init__(self, protocol, request):
        self._protocol = protocol
        self._request = request
        self._headers_sent = False

    def write(self, data):
        self._protocol._transport.write(b''.join([
            'HTTP/{} 200 OK\r\n'.format(
                self._request._version).encode('latin-1'),
            b'Content-Type: text/plain\r\n',
            'Content-Length: {}\r\n'.format(len(data)).encode('latin-1'),
            b'\r\n',
            data
        ]))


class HttpProtocol(asyncio.Protocol):

    __slots__ = ('_loop',
                 '_transport', '_current_request', '_current_parser',
                 '_current_url', '_current_headers')

    def __init__(self, *, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._transport = None
        self._current_request = None
        self._current_parser = None
        self._current_url = None
        self._current_headers = None

    def on_url(self, url):
        self._current_url = url

    def on_header(self, name, value):
        self._current_headers.append((name, value))

    def on_headers_complete(self):
        self._keep_alive = b'keep-alive' in [v for (k, v) in self._current_headers]
        self._current_request = HttpRequest(
            self, self._current_url, self._current_headers,
            self._current_parser.get_http_version())

        self._loop.call_soon(
            self.handle, self._current_request,
            HttpResponse(self, self._current_request))

    def connection_made(self, transport):
        self._transport = transport
        sock = transport.get_extra_info('socket')
        try:
            sock.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        except (OSError, NameError):
            pass

    def connection_lost(self, exc):
        self._current_request = self._current_parser = None

    def data_received(self, data):
        if self._current_parser is None:
            assert self._current_request is None
            self._current_headers = []
            self._current_parser = httptools.HttpRequestParser(self)

        self._current_parser.feed_data(data)

    def handle(self, request, response):
        async def somebody():
            return

        task = asyncio.ensure_future(somebody())
        asyncio.wait(task)
        response.write(b'Hello World!')

        if not self._keep_alive:
            self._transport.close()
        self._current_parser = None
        self._current_request = None


def httptools_server(loop, addr):
    return loop.create_server(lambda: HttpProtocol(loop=loop), *addr)


loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)
loop.set_debug(False)

server = loop.run_until_complete(httptools_server(loop, ('127.0.0.1', 8080)))
try:
    loop.run_forever()
finally:
    server.close()
    loop.close()
