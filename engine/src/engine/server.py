#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


class Server:
    def __init__(self, port):
        self.port = port
        self.host = '127.0.0.1'

    def run(self):
        conn, addr = self.s.accept()
        with conn:
            cmd = conn.recv(4, socket.MSG_WAITALL)

        if not cmd:
            return False

        self.command = int.from_bytes(cmd, 'little')
        if self.command == 255:
            return False

        return True

    def config(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen()
