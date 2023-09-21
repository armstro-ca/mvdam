import os
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

log_console_level = os.getenv('CONSOLELOGLEVEL') or logging.INFO
log_file_level = os.getenv('LOGLEVEL') or logging.DEBUG

log_filename = os.getenv('LOGFILE') or 'api.log'
log_file_format = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s')
log_console_format = logging.Formatter('%(asctime)s -  %(message)s')

console_handler = logging.StreamHandler(sys.stdout)
file_handler = TimedRotatingFileHandler(log_filename, when='midnight')


def get_console_handler():
    try:
        console_handler.setLevel(log_console_level)
    except ValueError as val_err:
        print(f'Logging level {val_err} is not a valid option. Please use one of the following:\
                DEBUG\
                INFO')
    console_handler.setFormatter(log_console_format)
    return console_handler


def get_file_handler():
    try:
        file_handler.setLevel(log_file_level)
    except ValueError as val_err:
        print(f'Logging level {val_err} is not a valid option. Please use one of the following:\
                DEBUG\
                INFO')    
    file_handler.setFormatter(log_file_format)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


def set_console_verbose():
    console_handler.setLevel(logging.DEBUG)
