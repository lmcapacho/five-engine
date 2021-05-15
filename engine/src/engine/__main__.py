#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from engine.engine import app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RISC-V engine emulator')
    parser.add_argument('port', help='Socket Port', type=int)
    args = parser.parse_args()
    app(args.port)
