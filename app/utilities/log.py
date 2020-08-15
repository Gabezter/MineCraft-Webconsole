import logging
from logging.handlers import TimedRotatingFileHandler
from enums import Loggers
import os
from flask import current_app
from datetime import datetime, timezone

log_file_main = os.path.join(
    current_app.config['LOG_LOCATION'], 'main/main.log')
log_file_debug = os.path.join(
    current_app.config['LOG_LOCATION'], 'debug/debug.log')
log_file_error_loc = os.path.join(current_app.config['LOG_LOCATION'], 'error/')

main = logging.getLogger('main-logger')
debug = logging.getLogger('debug-logger')


def get_debug_file_handler():
    fh = TimedRotatingFileHandler(log_file_debug, when='midnight')
    return fh


def get_main_file_handler():
    fh = TimedRotatingFileHandler(log_file_main, when='midnight')
    return fh


def get_logger(log_name):
    logger = logging.getLogger(log_name.name)
    if log_name == Loggers.Debug:
        logger.setLevel(logging.DEBUG)
        logger.addHandler(get_debug_file_handler())
    else:
        logger.setLevel(logging.INFO)
        logger.addHandler(get_main_file_handler())
    logger.propagate = False
    return logger


def generate_error_log(e):
    error_file = open(os.path.join(log_file_error_loc, str(datetime.now(timezone.utc)) + '.log'), 'w')
    error_file.write(e)
    error_file.close()


def setup_logging():
    if current_app.config['LOGGING']:
        try:
            os.mkdir(current_app.config['LOG_LOCATION'], mode=0o666)
            os.mkdir(os.path.join(current_app.config['LOG_LOCATION'], 'main'), mode=0o666)
            os.mkdir(os.path.join(current_app.config['LOG_LOCATION'], 'debug'), mode=0o666)
            os.mkdir(os.path.join(current_app.config['LOG_LOCATION'], 'error'), mode=0o666)
        except FileExistsError as e:
            print('Folders already made')
        except Exception as e:
            print(e)
    