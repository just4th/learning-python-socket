import typing
import socket

MAX_LOOP_ITERATIONS = 1000000
encoding = "ISO-8859-1"


class HeadersParser:
    _LENGTH_HEADER = "content-length"
    _RECV_BUFFER = 16
    _content_length: int
    _header_prefix: str
    _start_line: str
    _headers: typing.Dict[str, str] = {}
    _content: str

    def _reset(self):
        self._content_length = 0
        self._header_prefix = ''
        self._start_line = ''
        self._headers.clear()
        self._content = ''

    # returns not parsed line
    def _add_header(self) -> str | None:
        line = self._header_prefix
        self._header_prefix = ''
        if len(self._start_line) == 0:
            self._start_line = line
            return None

        i = line.find(':')
        if i == -1:
            return line

        key = line[:i].lower()
        value = line[i + 1:].lstrip()
        self._headers[key] = value

        if key == self._LENGTH_HEADER:
            self._content_length = int(value)
        return None

    def parse(self, s: socket.socket):
        self._reset()
        connection_closed = False
        for _ in range(MAX_LOOP_ITERATIONS):
            byte_data = s.recv(self._RECV_BUFFER)
            if byte_data == 0:
                connection_closed = True
                print('Error, connection closed')
                break

            data = self._header_prefix + byte_data.decode(encoding)
            self._header_prefix = ''

            left = 0
            has_empty_line = False
            for i in range(1, len(data)):
                if data[i] != '\n' or data[i - 1] != '\r':
                    continue

                self._header_prefix = data[left:i - 1]
                left = i + 1

                not_parsed = self._add_header()
                if not_parsed is None:
                    continue

                if len(not_parsed) == 0:
                    has_empty_line = True
                else:
                    print(f'Error, not a header: {not_parsed}')
                break

            self._header_prefix = data[left:]

            if not has_empty_line:
                continue

            if left != len(data):
                self._content = self._header_prefix
                self._header_prefix = ''
                break

        if connection_closed:
            return (self._headers, self._content)

        for _ in range(MAX_LOOP_ITERATIONS):
            if len(self._content) >= self._content_length:
                break
            byte_data = s.recv(self._RECV_BUFFER)
            if byte_data == 0:
                connection_closed = True
                print('Error, connection closed')
                break
            self._content += byte_data.decode(encoding)

        return (self._start_line, self._headers, self._content)
