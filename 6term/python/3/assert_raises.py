# -*- coding: utf-8 -*-

import sys


class AssertRaises:
    """Check if a specified exception is raised in code block inside this context manager"""

    def __init__(self, exc_type):
        self.exc_type = exc_type

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not self.exc_type:
            raise AssertionError
        return True


exec(sys.stdin.read())
