#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import shared_memory

from engine.server import Server


class GPIO:
    def __init__(self):
        self.shm = shared_memory.SharedMemory(create=True, size=4)

        self.server = Server(21234)
        self.server.config()

    def close(self):
        self.shm.close()
        self.shm.unlink()

    def sendID(self):
        self.server.open_conn()
        self.server.send_data(self.shm.name)

    def write(self, value):
        self.shm.buf[:4] = value.to_bytes(4, 'little')

    def read(self):
        value = self.shm.buf.tobytes()
        value = int.from_bytes(value, 'little')

        return value
