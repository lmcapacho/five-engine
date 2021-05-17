#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from .common import Cmd


class Server:
    def __init__(self, port):
        self.port = port
        self.host = '127.0.0.1'

    def wait_command(self):
        execute = True
        self.conn, addr = self.sock.accept()
        with self.conn:
            cmd = self.conn.recv(4, socket.MSG_WAITALL)
            cmd = int.from_bytes(cmd, 'little')

            if cmd == Cmd.EXIT:
                self.conn.sendall(int(0).to_bytes(4, 'little'))
                self.sock.close()
                execute = False

        return execute, cmd

    def config(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
