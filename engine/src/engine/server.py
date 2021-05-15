#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


class Server:
    def __init__(self, port):
        self.port = port
        self.host = '127.0.0.1'

    def run(self):
        execute = True
        conn, addr = self.sock.accept()
        with conn:
            cmd = conn.recv(4, socket.MSG_WAITALL)
            self.command = int.from_bytes(cmd, 'little')

            if self.command == 255:
                conn.sendall(int(0).to_bytes(4, 'little'))
                self.sock.close()
                execute = False

        return execute

    def config(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
