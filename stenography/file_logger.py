# coding: utf8
import os

from stenography import logger


class FileLogger(logger.Logger):
    def __init__(self, name=None, log_format=None, timestamp_format=None,
                 date_format=None, level=60, utc=False, filename_format=None,
                 logs_dir=None):
        super(FileLogger, self).__init__(
            name=name, log_format=log_format, timestamp_format=timestamp_format,
            date_format=date_format, level=level, utc=utc
        )
        self.filename_format = filename_format or '{date}_{name}.log'
        self.logs_dir = logs_dir

    def writeln(self, date, name, level, timestamp, msg, **kwargs):
        log_file = self.filename_format.format(date=date, name=name, level=level,
                                               timestamp=timestamp)
        log_file = os.path.join(self.logs_dir, log_file)

        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

        log_line = self.log_format.format(date=date, name=name, level=level,
                                          timestamp=timestamp, msg=msg)

        with open(log_file, 'a') as out:
            out.write('{}\n'.format(log_line))
