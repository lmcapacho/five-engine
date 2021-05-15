#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading

import pytest

from engine import engine


def run_engine():
    engine.app(4321)


@pytest.fixture(autouse=True)
def thread_engine():
    process = threading.Thread(target=run_engine)
    process.start()


def test_connection():
    HOST = '127.0.0.1'
    PORT = 4321
    data = b''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(int(255).to_bytes(4, 'little'))
        data = s.recv(4, socket.MSG_WAITALL)

    assert int.from_bytes(data, 'little') == 0
