# This Python file uses the following encoding: utf-8

import logging
import sys

DEFAULT_NAME_LENGTH = 22
DEFAULT_LOG_LEVEL = logging.DEBUG


def getLogger(**kwargs):
    if 'name' in kwargs:
        # create logger
        log = logging.getLogger(kwargs.get("name"))
    else:
        f = sys._current_frames().values()[0]
        log = logging.getLogger(f.f_back.f_globals['__name__'])

    if 'level' in kwargs:
        log.setLevel(kwargs.get("level"))
    else:
        log.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log