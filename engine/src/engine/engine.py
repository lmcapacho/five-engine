#!/usr/bin/env python
# -*- coding: utf-8 -*-


from engine.server import Server


def app(port):
    engine_server = Server(port)
    engine_server.config()

    while engine_server.run():
        pass
