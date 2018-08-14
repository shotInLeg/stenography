# coding: utf8
from stenography import logger


class CombinedLogger(logger.Logger):
    def __init__(self, name=None, log_format=None, timestamp_format=None,
                 date_format=None, level=60, utc=False, loggers=None):
        super(CombinedLogger, self).__init__(
            name=name, log_format=log_format, timestamp_format=timestamp_format,
            date_format=date_format, level=level, utc=utc
        )
        self.loggers = loggers or []

    def logging(self, level, msg, *args, **kwargs):
        for logger_ in self.loggers:
            logger_.logging(level, msg, *args, **kwargs)

    def writeln(self, date, name, level, timestamp, msg, *args, **kwargs):
        pass
