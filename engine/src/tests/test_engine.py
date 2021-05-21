#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
import time

import pytest

from engine.engine import Engine
from engine.common import Cmd


def run_engine():
    engine = Engine(4321)
    engine.app()


@pytest.fixture(autouse=True)
def thread_engine():
    process = threading.Thread(target=run_engine)
    process.start()


def test_connection():
    HOST = '127.0.0.1'
    PORT = 4321
    data = b''

    time.sleep(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((HOST, PORT))
        s.sendall(Cmd.EXIT.to_bytes(4, 'little'))
        data = s.recv(4, socket.MSG_WAITALL)

    assert int.from_bytes(data, 'little') == 0
