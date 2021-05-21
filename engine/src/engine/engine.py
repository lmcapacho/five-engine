#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import tempfile

from .common import Cmd, State
from engine.server import Server
from engine.debugger import Debugger
from engine.compiler import Compiler


class Engine:
    def __init__(self, port):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.curr_state = State.IDLE

        qemu_command = [
            'qemu-system-riscv32', '-s', '-S',
            '-nographic', '-machine', 'sifive_e'
        ]

        self.qemu = subprocess.Popen(
            qemu_command, stdin=subprocess.PIPE)
        self.server = Server(port)
        self.server.config()
        self.debugger = Debugger()
        self.debugger.connect()
        self.compiler = Compiler(self.temp_dir.name)

    def __del__(self):
        self.qemu.terminate()
        self.debugger.close()
        self.temp_dir.cleanup()

    def app(self):
        execute = True
        while execute:
            execute, cmd = self.server.wait_command()
            self.exec_cmd(cmd)

        self.qemu.terminate()
        self.debugger.close()

    def exec_cmd(self, cmd):
        if cmd == Cmd.LOAD:
            len = self.server.wait_data()
            code = self.server.wait_data(len)
            f = open(self.temp_dir+'/code.s', 'w')
            f.write(code)
            f.close()

            if self.curr_state == State.RUN:
                self.debugger.suspend()

            result = self.compiler.compile()
            if 'Error' in result:
                self.server.send_data(1)
            else:
                self.server.send_data(0)

            self.server.send_data(len(result))
            self.server.send_data(result)

            self.curr_state = State.LOAD

        elif cmd == Cmd.RUN:
            self.curr_state = Cmd.RUN
        elif cmd == Cmd.STEP:
            pass
        elif cmd == Cmd.PAUSE:
            self.curr_state = Cmd.PAUSE
        elif cmd == Cmd.STOP:
            self.curr_state = Cmd.IDLE
        elif cmd == Cmd.RESET:
            self.curr_state = Cmd.LOAD
        elif cmd == Cmd.BKP:
            pass
        elif cmd == Cmd.MEMORY:
            dir = self.server.wait_data()
            size = self.server.wait_data()
            msg, mem = self.debugger.readMemory(dir, size)
            if msg == 'error':
                self.server.send_data(2)
            else:
                self.server.send_data(0)
                self.server.send_data(mem)

        elif cmd == Cmd.GPIO_W:
            pass
        elif cmd == Cmd.GPIO_R:
            pass

        self.server.close_conn()
