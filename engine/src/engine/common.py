#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum


class Cmd(IntEnum):
    """ Commands """
    LOAD = 0
    RUN = 1
    STEP = 2
    PAUSE = 3
    STOP = 4
    RESET = 5
    BKP = 6
    MEMORY = 7
    GPIO_W = 8
    GPIO_R = 9
    EXIT = 255


class State(IntEnum):
    """ States """
    IDLE = 0
    LOAD = 1
    RUN = 2
    PAUSE = 3
