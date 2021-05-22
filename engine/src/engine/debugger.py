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

    def run(self):
        response = self.gdbmi.write('c')
        return response

    def step(self):
        self.gdbmi.write('s')
        status = self.getStatus()
        return status

    def loadCode(self, filename):
        gdb_cmd = f'add-symbol-file {filename}'
        response = self.gdbmi.write(gdb_cmd)
        gdb_cmd = f'load {filename}'
        response = self.gdbmi.write(gdb_cmd)
        return response

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

    def getStatus(self):
        response = self.gdbmi.write('frame')
        for res in response:
            if res['type'] == 'console':
                if res['payload'] in ':':
                    line = res['payload'].split(':')[1]
                    line = line.split('\\')[0]
                    line = int(line)
                else:
                    line = 0

        response = self.gdbmi.write('info registers')
        regs = []
        for res in response:
            if res['type'] == 'console':
                reg = res['payload'].split()[1]
                reg = reg.split('\\')[0]
                regs.append(int(reg, 16))

        status = regs
        status.append(line)

        return status

    def close(self):
        if self.gdbmi is not None:
            self.gdbmi.exit()
