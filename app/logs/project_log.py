"""Module for file logging"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler

log_formatter = logging.Formatter('%(asctime)s <%(module)s> %(levelname)s '
                                  '%(funcName)s(%(lineno)d) %(message)s')

os.makedirs('logs_all', exist_ok=True)
LOG_FILE = 'logs_all/service.log'

log_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight", backupCount=31)

log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)
log_handler.suffix = "%Y_%m_%d"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(log_formatter)
logger.addHandler(consoleHandler)
