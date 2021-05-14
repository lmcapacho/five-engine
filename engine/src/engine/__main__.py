#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from engine.server import Server


def main(port):
    engine_server = Server(port)
    engine_server.config()

    while engine_server.run():
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RISC-V engine emulator')
    parser.add_argument('port', help='Socket Port', type=int, default=4321)
    args = parser.parse_args()
    main(args.port)
