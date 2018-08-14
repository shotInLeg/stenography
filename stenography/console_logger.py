# coding: utf8
from stenography import logger


class ConsoleLogger(logger.Logger):
    def writeln(self, date, name, level, timestamp, msg, *args, **kwargs):
        log_line = self.log_format.format(date=date, name=name, level=level,
                                          timestamp=timestamp, msg=msg)
        print(log_line)
