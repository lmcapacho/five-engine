#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import os


class Compiler:
    def __init__(self, dir):
        dirname = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))) + '/resources/'
        self.as_command = [
            'riscv64-unknown-elf-as', '-g', '-march',
            'rv32imac', '-o', dir+'/code.o',
            dir + '/code.s', '-statistics'
        ]

        self.ld_command = [
            'riscv64-unknown-elf-ld', '-g', '-m',
            'elf32lriscv', '-T', dirname+'link.lds', '-o',
            dir+'/code', dir+'/code.o',
            '-print-memory-usage'
        ]

    def compile(self):
        assembler = subprocess.Popen(
            self.as_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        result = assembler.stdout.read()

        linker = subprocess.Popen(
            self.ld_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        result += linker.stdout.read()

        return result.decode()
