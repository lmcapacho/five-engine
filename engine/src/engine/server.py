#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from .common import Cmd, State


class Server:
    def __init__(self, port):
        self.port = port
        self.host = '127.0.0.1'
        self.curr_state = State.IDLE

    def run(self):
        execute = True
        self.conn, addr = self.sock.accept()
        with self.conn:
            cmd = self.conn.recv(4, socket.MSG_WAITALL)
            self.command = int.from_bytes(cmd, 'little')

            if self.command == Cmd.EXIT:
                self.conn.sendall(int(0).to_bytes(4, 'little'))
                self.sock.close()
                execute = False

        return execute

    def parser(self):
        if self.command == Cmd.LOAD:
            self.curr_state = Cmd.LOAD
        elif self.command == Cmd.RUN:
            self.curr_state = Cmd.RUN
        elif self.command == Cmd.STEP:
            pass
        elif self.command == Cmd.PAUSE:
            self.curr_state = Cmd.PAUSE
        elif self.command == Cmd.STOP:
            self.curr_state = Cmd.IDLE
        elif self.command == Cmd.RESET:
            self.curr_state = Cmd.LOAD
        elif self.command == Cmd.BKP:
            pass
        elif self.command == Cmd.MEMORY:
            pass
        elif self.command == Cmd.GPIO_W:
            pass
        elif self.command == Cmd.GPIO_R:
            pass

    def config(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
