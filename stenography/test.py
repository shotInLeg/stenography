# coding: utf8
import time
import context
import decorators
import logging

logging.basicConfig(level=logging.INFO)

@decorators.worktime_log('root', None)
def main():
    with context.WorktimeLog('root', None, 'for'):
        for _ in range(3):
            time.sleep(1)


if __name__ == '__main__':
    main()
