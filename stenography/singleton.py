# coding: utf8
from stenography import console_logger


class LoggerSingleton(object):
    loggers = {}

    def __init__(self):
        raise NotImplemented('This object is singleton')

    @staticmethod
    def get_logger(name='stenography', logger=None, **kwargs):
        if logger is None and name not in LoggerSingleton.loggers:
            LoggerSingleton.loggers[name] = console_logger.ConsoleLogger(name=name)

        elif logger is not None and name not in LoggerSingleton.loggers:
            LoggerSingleton.loggers[name] = logger(name=name, **kwargs)

        elif logger is not None and not isinstance(LoggerSingleton.loggers[name], logger):
            LoggerSingleton.loggers[name] = logger(name=name, **kwargs)

        return LoggerSingleton.loggers[name]
