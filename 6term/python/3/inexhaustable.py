# -*- coding: utf-8 -*-

import sys
import functools


class Inexhaustable:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        return self.func(*self.args, **self.kwargs)


def inexhaustable(func):
    """Decorate generator function to be inexhaustible

    :param func: a function to decorate
    :return: decorated function
    """

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        return Inexhaustable(func, *args, **kwargs)

    return decorated


exec(sys.stdin.read())
