#!/usr/bin/env python
# -*- coding: utf-8 -*-

from engine.server import Server


def main():
    engine_server = Server()
    engine_server.config()

    while engine_server.run():
        pass


if __name__ == '__main__':
    main()
