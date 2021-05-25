#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import tempfile

from .common import Cmd, State
from engine.server import Server
from engine.debugger import Debugger
from engine.compiler import Compiler
from engine.gpio import GPIO


class Engine:
    def __init__(self, port):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.curr_state = State.IDLE

        qemu_command = [
            'qemu-system-riscv32', '-s', '-S',
            '-nographic', '-machine', 'sifive_e'
        ]

        self.gpio = GPIO()
        self.qemu = subprocess.Popen(
            qemu_command, stdin=subprocess.PIPE)
        self.server = Server(port)
        self.server.config()
        self.debugger = Debugger()
        self.debugger.connect()
        self.compiler = Compiler(self.temp_dir.name)
        self.gpio.sendID()

    def __del__(self):
        self.qemu.terminate()
        self.debugger.close()
        self.temp_dir.cleanup()

    def app(self):
        self.execute = True
        while self.execute:
            self.server.open_conn()
            cmd = self.server.read_data()
            self.exec_cmd(cmd)

        self.qemu.terminate()
        self.debugger.close()
        self.gpio.close()

    def exec_cmd(self, cmd):
        if cmd == Cmd.LOAD:
            size = self.server.read_data()
            code = self.server.read_data(str, size)
            f = open(self.temp_dir.name+'/code.s', 'w')
            f.write(code)
            f.close()

            result = self.compiler.compile()
            if 'Error' in result:
                self.server.send_data(1)
            else:
                if self.curr_state == State.RUN:
                    self.debugger.suspend()

                self.debugger.loadCode(self.temp_dir.name+'/code')
                self.server.send_data(0)
                self.curr_state = State.LOAD

            self.server.send_data(len(result))
            self.server.send_data(result)

        elif cmd == Cmd.RUN:
            if self.curr_state == State.LOAD or self.curr_state == State.PAUSE:
                self.debugger.run()
                self.server.send_data(0)
                self.curr_state = State.RUN
            else:
                self.server.send_data(1)

        elif cmd == Cmd.STEP:
            if self.curr_state == State.LOAD or self.curr_state == State.PAUSE:
                status = self.debugger.step()
                self.server.send_data(0)
                self.server.send_data(status)
            else:
                self.server.send_data(1)

        elif cmd == Cmd.PAUSE:
            if self.curr_state == State.RUN:
                self.debugger.suspend()
                status = self.debugger.getStatus()
                self.server.send_data(0)
                self.server.send_data(status)
                self.curr_state = State.PAUSE
            else:
                self.server.send_data(1)

        elif cmd == Cmd.STOP:
            if self.curr_state == State.RUN or self.curr_state == State.PAUSE:
                if self.curr_state == State.RUN:
                    self.debugger.suspend()
                status = self.debugger.getStatus()
                self.server.send_data(0)
                self.server.send_data(status)
                self.curr_state = State.IDLE
            else:
                self.server.send_data(1)

        elif cmd == Cmd.RESET:
            if self.curr_state == State.RUN:
                self.debugger.suspend()

            self.debugger.loadCode(self.temp_dir.name+'/code')
            status = self.debugger.getStatus()
            self.server.send_data(0)
            self.server.send_data(status)

            self.curr_state = State.LOAD

        elif cmd == Cmd.BKP:
            line = self.server.read_data()
            if self.curr_state != State.IDLE:
                self.debugger.breakpoint(line)
                self.server.send_data(0)
            else:
                self.server.send_data(1)

        elif cmd == Cmd.MEMORY:
            dir = self.server.read_data()
            size = self.server.read_data()
            if self.curr_state == State.LOAD or self.curr_state == State.PAUSE:
                msg, mem = self.debugger.readMemory(dir, size)
                if msg == 'error':
                    self.server.send_data(2)
                else:
                    self.server.send_data(0)
                    self.server.send_data(mem)
            else:
                self.server.send_data(1)

        elif cmd == Cmd.GPIO_W:
            value = self.server.read_data()
            self.gpio.write(value)
            self.server.send_data(0)

        elif cmd == Cmd.GPIO_R:
            value = self.gpio.read()
            self.server.send_data(0)
            self.server.send_data(value)

        elif cmd == Cmd.EXIT:
            self.server.send_data(0)
            self.server.close()
            self.execute = False

        self.server.close_conn()
