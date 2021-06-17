#!/usr/bin/env python3

from .lan_fabric import api as core


class api(core):
    def __init__(self, conn):
        core.__init__(self, conn)
