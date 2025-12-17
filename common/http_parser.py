import typing
import socket

MAX_LOOP_ITERATIONS = 1000000
encoding = "ISO-8859-1"


class HeadersParser:
    __length_header = "content-length"
    __recv_buffer = 16
    __content_length: int
    __header_prefix: str
    __start_line: str
    __headers: typing.Dict[str, str] = {}
    __content: str

    def __reset(self):
        self.__content_length = 0
        self.__header_prefix = ''
        self.__start_line = ''
        self.__headers.clear()
        self.__content = ''

    # returns not parsed line
    def __add_header(self) -> str | None:
        line = self.__header_prefix
        self.__header_prefix = ''
        if len(self.__start_line) == 0:
            self.__start_line = line
            return None

        i = line.find(':')
        if i == -1:
            return line

        key = line[:i].lower()
        value = line[i + 1:].lstrip()
        self.__headers[key] = value

        if key == self.__length_header:
            self.__content_length = int(value)
        return None

    def parse(self, s: socket.socket):
        self.__reset()
        connection_closed = False
        for _ in range(MAX_LOOP_ITERATIONS):
            byte_data = s.recv(self.__recv_buffer)
            if byte_data == 0:
                connection_closed = True
                print('Error, connection closed')
                break

            data = self.__header_prefix + byte_data.decode(encoding)
            self.__header_prefix = ''

            left = 0
            has_empty_line = False
            for i in range(1, len(data)):
                if data[i] != '\n' or data[i - 1] != '\r':
                    continue

                self.__header_prefix = data[left:i - 1]
                left = i + 1

                not_parsed = self.__add_header()
                if not_parsed is None:
                    continue

                if len(not_parsed) == 0:
                    has_empty_line = True
                else:
                    print(f'Error, not a header: {not_parsed}')
                break

            self.__header_prefix = data[left:]

            if not has_empty_line:
                continue

            if left != len(data):
                self.__content = self.__header_prefix
                self.__header_prefix = ''
                break

        if connection_closed:
            return (self.__headers, self.__content)

        for _ in range(MAX_LOOP_ITERATIONS):
            if len(self.__content) >= self.__content_length:
                break
            byte_data = s.recv(self.__recv_buffer)
            if byte_data == 0:
                connection_closed = True
                print('Error, connection closed')
                break
            self.__content += byte_data.decode(encoding)

        return (self.__start_line, self.__headers, self.__content)
