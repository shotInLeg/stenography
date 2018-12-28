# coding: utf8
import time
import logging
import inspect
import functools
import traceback


def worktime_log(logger_name, level=logging.DEBUG):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                ret_value = func(*args, **kwargs)
            finally:
                logging.getLogger(logger_name).info(
                    'WORKTIME f@{} by {}s'.format(func.__name__, time.time() - start)
                )
            return ret_value
        return wrapper
    return decorator


def function_call_log(logger_name, level=logging.DEBUG, finish=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(logger_name)
            caller = inspect.stack()[1][3]
            code_row = inspect.stack()[1][2]
            start = time.time()
            try:
                logger.info(
                    'FUNCTION_CALL CALL f@{}[LINE:{}] -> f@{}'.format(caller, code_row, func.__name__)
                )
                ret_value = func(*args, **kwargs)
            finally:
                if finish:
                    logger.info(
                        'FUNCTION_CALL RETURN f@{}[LINE:{}] <- f@{} by {}s'.format(caller, code_row, func.__name__, time.time() - start)
                    )
            return ret_value
        return wrapper
    return decorator


def raise_log(logger_name, level=logging.DEBUG, trace=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(logger_name)
            try:
                ret_value = func(*args, **kwargs)
            except Exception as e:
                if not trace:
                    logger.error(
                        'RAISE EXCEPTION {}(f@{}) {}'.format(type(e), func.__name__, e)
                    )
                else:
                    logger.error(
                        'RAISE TRACEBACK f@{}\n{}\n{}'.format(
                            func.__name__, traceback.format_exc(limit=20),
                            '-' * 80
                        )
                    )
                raise
            return ret_value
        return wrapper
    return decorator


def warnslow_log(logger_name, level=logging.DEBUG, speed=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(logger_name)
            start = time.time()
            try:
                ret_value = func(*args, **kwargs)
            finally:
                delta = time.time() - start
                if delta > speed:
                    logger.warn('WARNSLOW f@{} by {}s'.format(func.__name__, delta))
            return ret_value
        return wrapper
    return decorator


def warnvalue(logger_name, level=logging.DEBUG, print_ret_value=False, comp=lambda x: x is None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = logging.getLogger(logger_name)
            ret_value = None
            try:
                ret_value = func(*args, **kwargs)
            finally:
                if comp(ret_value):
                    logger.warn('WARNVALUE f@{}{}'.format(
                        func.__name__, ' {}'.format(ret_value) if print_ret_value else ''
                    ))
            return ret_value
        return wrapper
    return decorator

