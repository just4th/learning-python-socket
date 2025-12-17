#!/usr/bin/env python3

import argparse

from impl.web_server.web_server import run_web_server


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-p', '--port',
        default='28333',
        type=int
    )

    args = parser.parse_args()

    run_web_server(args.port)


if __name__ == '__main__':
    main()
