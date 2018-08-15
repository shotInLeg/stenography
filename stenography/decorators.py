# coding: utf8
import time
import inspect
import functools
import traceback

import singleton


def worktime(logger_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                ret_value = func(*args, **kwargs)
            finally:
                singleton.LoggerSingleton.get_logger(logger_name).info(
                    'TIME {} {}'.format(func.__name__, time.time() - start)
                )
            return ret_value
        return wrapper
    return decorator


def raiselog(logger_name, trace=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                ret_value = func(*args, **kwargs)
            except Exception as e:
                if not trace:
                    singleton.LoggerSingleton.get_logger(logger_name).error(
                        '{}({}) {}'.format(type(e), func.__name__, e)
                    )
                else:
                    singleton.LoggerSingleton.get_logger(logger_name).error(
                        'TRACEBACK {}\n{}\n{}'.format(
                            func.__name__, traceback.format_exc(limit=20),
                            '-' * 80
                        )
                    )
                raise
            return ret_value
        return wrapper
    return decorator


def calllog(logger_name, finish=False, work_time=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            caller = inspect.stack()[1][3]
            row = inspect.stack()[1][2]
            start = time.time()
            try:
                singleton.LoggerSingleton.get_logger(logger_name).debug(
                    'CALL {}[{}] -> {}'.format(caller, row, func.__name__)
                )
                ret_value = func(*args, **kwargs)
            finally:
                if finish:
                    singleton.LoggerSingleton.get_logger(logger_name).debug(
                        'RETURN {}[{}] <- {}{}'.format(
                            caller, row, func.__name__,
                            ' {}'.format(time.time() - start) if work_time else ''
                        )
                    )
                elif work_time:
                    singleton.LoggerSingleton.get_logger(logger_name).debug(
                        'TIME {} {}'.format(func.__name__, time.time() - start)
                    )
            return ret_value
        return wrapper
    return decorator


def warnslow(logger_name, speed=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                ret_value = func(*args, **kwargs)
            finally:
                delta = time.time() - start
                if delta > speed:
                    singleton.LoggerSingleton.get_logger(logger_name).warn(
                        'SLOW {} {}'.format(func.__name__, delta)
                    )
            return ret_value
        return wrapper
    return decorator


def warnvalue(logger_name, value=1, comp=lambda x, y: x == y):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ret_value = None
            try:
                ret_value = func(*args, **kwargs)
            finally:
                if comp(ret_value, value):
                    singleton.LoggerSingleton.get_logger(logger_name).warn(
                        'BAD RETURN {}'.format(func.__name__)
                    )
            return ret_value
        return wrapper
    return decorator


def combined(*decorators):
    def decorator(func):
        new_func = func
        for decor in reversed(decorators):
            new_func = decor(new_func)
            new_func.__name__ = func.__name__
        return new_func
    return decorator
