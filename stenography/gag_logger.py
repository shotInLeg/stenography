# coding: utf8
from stenography import logger


class GagLogger(logger.Logger):
    def writeln(self, date, name, level, timestamp, msg, **kwargs):
        pass
