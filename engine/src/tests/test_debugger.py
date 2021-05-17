#!/usr/bin/env python
# -*- coding: utf-8 -*-

from engine import debugger


def test_run():
    gdb = debugger.Debugger()
    assert gdb.gdbmi is not None
