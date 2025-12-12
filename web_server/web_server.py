import socket
import sys
import lib.http_parser

encoding = "ISO-8859-1"
max_loop_iterations = 1000000
header_parser = lib.http_parser.HeadersParser()


def read_args() -> list[str]:
    args = ['28333']
    for i in range(min(len(args), len(sys.argv) - 1)):
        args[i] = sys.argv[i + 1]
    return args


def handle_connection(s):
    try:
        new_con = s.accept()
    except:
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


def main():
    args = read_args()
    port = int(args[0])
    with socket.socket() as s:
        s.settimeout(3)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen()
        while True:
            handle_connection(s)
    
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')