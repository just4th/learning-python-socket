import sys
import socket


def read_args():
    args = ['example.com', '80']
    for i in range(min(len(args), len(sys.argv) - 1)):
        args[i] = sys.argv[i + 1]
    return args


def main():
    ENCODING = "ISO-8859-1"

    print(socket.gethostbyname("www.google.com"))

    args = read_args()
    dest = (args[0], int(args[1]))

    with socket.socket() as s:
        s.connect(dest)

        content = 'qwertyuiopasdfghjklzxcvbnm'
        headers = [
            'GET / HTTP/1.1',
            f'Host: {args[0]}',
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


if __name__ == "__main__":
    main()
