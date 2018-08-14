# coding: utf8
import datetime

CRITICAL = 100
ERROR = 90
TRACEBACK = 80
WARNING = 70
INFO = 60
DEBUG = 50
NOTSET = 40

LEVEL_TO_NAME = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    TRACEBACK: 'TRACEBACK',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET'
}

NAME_TO_LEVEL = {
    'CRITICAL': CRITICAL,
    'ERROR': ERROR,
    'TRACEBACK': TRACEBACK,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET
}


class Logger(object):
    def __init__(self, name=None, log_format=None, timestamp_format=None,
                 date_format=None, level=60, utc=False):
        self.name = name or 'stenography'
        self.log_format = log_format or '{level}\t{name}\t{timestamp}\t{msg}'
        self.timestamp_format = timestamp_format or '%Y-%m-%dT%H:%M:%S'
        self.date_format = date_format or '%Y-%m-%d'
        self.level = level
        self.utc = utc

    @staticmethod
    def prepare_msg(msg):
        return msg.replace('\t', '    ').replace('\n', '\%n')

    def is_enable(self, level=None, level_name=None):
        level = level or NAME_TO_LEVEL[level_name]
        return level >= self.level

    def debug(self, msg, *args, **kwargs):
        if self.is_enable(DEBUG):
            self.logging(DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.is_enable(INFO):
            self.logging(INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.is_enable(WARNING):
            self.logging(INFO, msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.is_enable(ERROR):
            self.logging(ERROR, msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        if self.is_enable(ERROR):
            self.logging(ERROR, msg, *args, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.is_enable(CRITICAL):
            self.logging(CRITICAL, msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        self.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        if self.is_enable(level):
            self.logging(level, msg, *args, **kwargs)

    def logging(self, level, msg, *args, **kwargs):
        now = datetime.datetime.utcnow() if self.utc else \
            datetime.datetime.now()
        date = now.strftime(self.date_format)
        timestamp = now.strftime(self.timestamp_format)

        self.writeln(date, self.name, LEVEL_TO_NAME[level], timestamp,
                     self.prepare_msg(msg), *args, **kwargs)

    def writeln(self, date, name, level, timestamp, msg, *args, **kwargs):
        raise NotImplementedError('This method need to implement')
