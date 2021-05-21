#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pygdbmi.gdbcontroller import GdbController


class Debugger:
    def __init__(self, arch='riscv:rv32'):
        # logging.basicConfig(level=logging.DEBUG)
        self.gdbmi = None
        try:
            command = ['gdb-multiarch', '--interpreter=mi3', '--quiet']
            self.gdbmi = GdbController(command)
        except ValueError as msg:
            logging.critical(msg)

        if self.gdbmi is not None:
            self.gdbmi.write('set confirm off')
            self.gdbmi.write('set architecture '+arch)

    def __del__(self):
        self.close()

    def connect(self):
        if self.gdbmi is not None:
            self.gdbmi.write('target remote :1234')

    def suspend(self):
        self.gdbmi.send_signal_to_gdb('SIGINT')

    def loadCode(self, filename):
        gdb_cmd = f'add-symbol-file {filename}'
        response = self.gdbmi.write(gdb_cmd)
        gdb_cmd = f'load {filename}'
        response = self.gdbmi.write(gdb_cmd)

    def readMemory(self, dir, size):
        gdb_cmd = f'x/{size} {dir}'
        response = self.gdbmi.write(gdb_cmd)

        for res in response:
            if res['type'] == 'result':
                msg = res['message']
                if res['payload'] is not None:
                    payload = res['payload']['msg'].encode()
                else:
                    payload = None

        return msg, payload

    def close(self):
        if self.gdbmi is not None:
            self.gdbmi.exit()
