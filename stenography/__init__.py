# !/usr/bin/env python
# coding: utf8
"""Initialize module utils."""
__all__ = [
    'CombinedLogger',
    'ConsoleLogger',
    'FileLogger',
    'LoggerSingleton'
]


from .combined_logger import CombinedLogger
from .console_logger import ConsoleLogger
from .file_logger import FileLogger
from .singleton import LoggerSingleton

__version__ = '0.0.1'


def get(name=None, logger=None, **kwargs):
    return LoggerSingleton.get_logger(name, logger, **kwargs)


def on_import():
    import os
    import json

    settings = 'stenography.settings.json'

    name_to_logger = {
        'console': ConsoleLogger,
        'file': FileLogger
    }

    if not os.path.exists(settings):
        return

    with open(settings, 'r') as file:
        settings_data = json.dumps(file.read())

    for logger_name, list_loggers in settings_data.items():
        loggers = []
        for logger_settings in list_loggers:
            loggers.append({
                'logger': name_to_logger[logger_settings['type']],
                'kwargs': logger_settings['kwargs']
            })

        if len(loggers) > 1:
            get(logger_name, CombinedLogger, loggers=[
                x['logger'](name=logger_name, **x['kwargs']) for x in loggers
            ])
        elif len(loggers) == 1:
            get(logger_name, loggers[0]['logger'], **loggers[0]['kwargs'])


on_import()
