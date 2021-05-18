#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading

import pytest

from engine.server import Server
from engine.common import Cmd


def run_server():
    engine_server = Server(4321)
    engine_server.config()

    execute = True
    while execute:
        execute, cmd = engine_server.wait_command()


@pytest.fixture(autouse=True)
def thread_engine():
    process = threading.Thread(target=run_server)
    process.start()


def test_connection():
    HOST = '127.0.0.1'
    PORT = 4321
    data = b''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((HOST, PORT))
        s.sendall(Cmd.EXIT.to_bytes(4, 'little'))
        data = s.recv(4, socket.MSG_WAITALL)

    assert int.from_bytes(data, 'little') == 0
