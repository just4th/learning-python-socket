#!/usr/bin/env python3

import socket
from impl.common.http_parser import HeadersParser

encoding = "ISO-8859-1"
header_parser = HeadersParser()


def handle_connection(s):
    try:
        new_con = s.accept()
    except Exception as e:
        print(f'Exception: {e}')
        return

    with new_con[0] as new_soc:
        start_line_req, headers_req, content_req = header_parser.parse(new_soc)

        print(f'START LINE\n{start_line_req}\n')
        print(f'HEADERS\n{headers_req}\n')
        print(f'CONTENT\n{content_req}\n')
        print()

        content_resp = f'Here is your content: {{\n{content_req}\n}}'
        headers_resp = [
            'HTTP/1.1 200 OK',
            'Content-Type: text/plain',
            f'Content-Length: {len(content_resp)}',
            'Connection: close',
            '',
            content_resp
        ]
        resp = '\r\n'.join(headers_resp)

        print(f'RESPONSE\n{resp}\n')
        new_soc.send(resp.encode(encoding))


def run_web_server(port: int):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen()
        while True:
            handle_connection(s)
