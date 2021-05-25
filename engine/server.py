#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


class Server:
    def __init__(self, port):
        self.port = port
        self.host = '127.0.0.1'

    def open_conn(self):
        self.conn, _ = self.sock.accept()

    def read_data(self, type=int, size=4):
        data = self.conn.recv(size, socket.MSG_WAITALL)
        if type == int:
            data = int.from_bytes(data, 'little')
        elif type == str:
            data = data.decode()

        return data

    def send_data(self, data):
        if isinstance(data, int):
            value = data.to_bytes(4, 'little')
        elif isinstance(data, str):
            value = data.encode()
        elif isinstance(data, list):
            value = b''
            for d in data:
                value += d.to_bytes(4, 'little')
        else:
            value = b''

        self.conn.sendall(value)

    def close(self):
        self.conn.close()
        self.sock.close()

    def close_conn(self):
        self.conn.close()

    def config(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
