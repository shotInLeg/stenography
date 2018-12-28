# coding: utf8
import time
import inspect
import logging


def _get_caller_info(level):
    path = inspect.stack()[level + 1][1]
    line = inspect.stack()[level + 1][2]
    name = inspect.stack()[level + 1][3]
    return path, name, line


class ContextLogger(object):
    def __init__(self, logger_name, level, block_name):
        self.logger = logging.getLogger(logger_name)
        self.level = level
        self.block_name = block_name
        self.caller_path, self.caller_name, self.caller_line = _get_caller_info(2)

    def __enter__(self):
        raise NotImplementedError('This method must be implemented')

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError('This method must be implemented')


class WorktimeLog(ContextLogger):
    def __init__(self, logger_name, level, block_name='block'):
        super(WorktimeLog, self).__init__(logger_name, level, block_name)
        self.start = None

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info('WORKTIME b@{} by {}s ({} {} {})'.format(
            self.block_name, time.time() - self.start, self.caller_path, self.caller_name,
            self.caller_line
        ))

