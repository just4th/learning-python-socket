#!/usr/bin/env python3

import argparse

from impl.web_client.web_client import run_web_client


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--host',
        default='example.com'
    )

    parser.add_argument(
        '-p', '--port',
        default='80',
        type=int
    )

    args = parser.parse_args()

    run_web_client(args.host, args.port)


if __name__ == '__main__':
    main()
