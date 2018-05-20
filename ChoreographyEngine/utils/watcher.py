#! python3
# coding: utf-8

import os
import signal
import sys

"""
The `Watcher` class can only run on Linux, MacOS (Darwin) and other POSIX OS now.
"""


class Watcher:

    def __init__(self):
        self.child = os.fork()
        if self.child == 0:
            return
        else:
            self.__watch()

    def __watch(self):
        try:
            os.wait()
        except KeyboardInterrupt:
            self.__kill()
        sys.exit()

    def __kill(self):
        try:
            os.kill(self.child, signal.SIGKILL)
        except OSError as e:
            print(e)
