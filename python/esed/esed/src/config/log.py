import logging
from config import conf
from logging.handlers import QueueHandler

class MyLogger(object):
    def __init__(self, name, format="%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s", level=logging.DEBUG):
        # Initial construct.
        self.format = format
        self.level = level
        self.name = name
        
        # Complete logging config.
        self.logger = logging.getLogger(self.name)
        if (self.logger.hasHandlers()):
            self.logger.handlers.clear()
        self.logger.setLevel(self.level) 

        # Logger configuration
        self.console_logger = logging.handlers.RotatingFileHandler(filename=conf.log_folder, encoding=None)
        self.console_logger.setFormatter(logging.Formatter('%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'))
        self.console_logger.setLevel(logging.DEBUG)

        self.logger.addHandler(self.console_logger) 

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)

    def warn(self, msg, extra=None):
        self.logger.warn(msg, extra=extra)


