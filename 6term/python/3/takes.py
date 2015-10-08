# -*- coding: utf-8 -*-

import sys
import functools


def takes(*types):
    """Decorate function to specify and check types of arguments

    :param types: class types of arguments
    :return: decorated function
    """

    def decorator(func):

        @functools.wraps(func)
        def decorated(*args):
            for arg, type_ in zip(args, types):
                if type(arg) is not type_:
                    raise TypeError
            return func(*args)

        return decorated

    return decorator


exec(sys.stdin.read())
