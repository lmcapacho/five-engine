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

        cmd = self.conn.recv(4, socket.MSG_WAITALL)
        cmd = int.from_bytes(cmd, 'little')

        if cmd == Cmd.EXIT:
            self.conn.sendall(int(0).to_bytes(4, 'little'))
            self.conn.close()
            self.sock.close()
            execute = False

        return execute, cmd

    def wait_data(self, size=4):
        data = self.conn.recv(size, socket.MSG_WAITALL)
        data = int.from_bytes(data, 'little')

        return data

    def send_data(self, data):
        if isinstance(data, int):
            data = data.to_bytes(4, 'little')
        elif isinstance(data, str):
            data = data.decode()
        else:
            data = b''

        self.conn.sendall(data)

    def close_conn(self):
        self.conn.close()

    def config(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
