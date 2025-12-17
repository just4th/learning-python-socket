import socket


def run_web_client(host: str, port: int) -> None:
    ENCODING = "ISO-8859-1"

    print(socket.gethostbyname("www.google.com"))

    with socket.socket() as s:
        s.connect((host, port))

        content = 'qwertyuiopasdfghjklzxcvbnm'
        headers = [
            'GET / HTTP/1.1',
            f'Host: {host}',
            f'Content-Length: {len(content)}',
            'Connection: close',
            '',
            content
        ]
        request = '\r\n'.join(headers)

        print(request)

        s.sendall(request.encode(ENCODING))

        resp_bytes = []
        while True:
            d = s.recv(16)
            if len(d) == 0:
                break
            resp_bytes.append(d)

        resp = ''.join([x.decode(ENCODING) for x in resp_bytes])

        print(resp)
