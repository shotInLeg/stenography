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
                 date_format=None, level=INFO, utc=False):
        self.name = name or 'stenography'
        self.log_format = log_format or '{level}\t{name}\t{timestamp}\t{msg}'
        self.timestamp_format = timestamp_format or '%Y-%m-%dT%H:%M:%S'
        self.date_format = date_format or '%Y-%m-%d'
        self.level = level
        self.utc = utc

    @staticmethod
    def prepare_msg(msg):
        return msg.replace('\t', '    ').replace('\n', '\%n')

    @staticmethod
    def add_level(value, name):
        if value in LEVEL_TO_NAME or name in NAME_TO_LEVEL:
            return
        LEVEL_TO_NAME[value] = name
        NAME_TO_LEVEL[name] = value

    def is_enable(self, level=None, level_name=None):
        level = level or NAME_TO_LEVEL[level_name]
        return level >= self.level

    def debug(self, msg, *args, **kwargs):
        if self.is_enable(DEBUG):
            self.logging(DEBUG, msg, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.is_enable(INFO):
            self.logging(INFO, msg, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.is_enable(WARNING):
            self.logging(INFO, msg, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.is_enable(ERROR):
            self.logging(ERROR, msg, **kwargs)

    def exception(self, msg, *args, **kwargs):
        if self.is_enable(ERROR):
            exc_info = kwargs.get('exc_info', True)
            self.logging(ERROR, msg, exc_info=exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.is_enable(CRITICAL):
            self.logging(CRITICAL, msg, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        self.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        if self.is_enable(level):
            self.logging(level, msg, **kwargs)

    def logging(self, level, msg, **kwargs):
        now = datetime.datetime.utcnow() if self.utc else \
            datetime.datetime.now()
        date = now.strftime(self.date_format)
        timestamp = now.strftime(self.timestamp_format)
        lst_key_value = []
        for key, value in kwargs.iteritems():
            lst_key_value.append('{}={}'.format(key, value))
        msg = '\t'.join(lst_key_value) or self.prepare_msg(msg)

        self.writeln(date, self.name, LEVEL_TO_NAME[level], timestamp,
                     msg, **kwargs)

    def writeln(self, date, name, level, timestamp, msg, **kwargs):
        raise NotImplementedError('This method need to implement')
