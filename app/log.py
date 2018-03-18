import os
import logging
from logging.handlers import RotatingFileHandler


class Log(object):
    def __init__(self, path='../logs'):
        self.path = path

    def not_exist_makedirs(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def init_app(self, app):
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        )

        log_dir = os.path.join(app.root_path, self.path)
        self.not_exist_makedirs(log_dir)

        debug_log = os.path.join(log_dir, 'debug.log')
        debug_file_handler = RotatingFileHandler(
            debug_log, maxBytes=100000, backupCount=10, delay=True
        )

        debug_file_handler.setLevel(logging.INFO)
        debug_file_handler.setFormatter(formatter)
        app.logger.addHandler(debug_file_handler)

        error_log = os.path.join(log_dir, 'error.log')
        error_file_handler = RotatingFileHandler(
            error_log, maxBytes=100000, backupCount=10
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)
        app.logger.addHandler(error_file_handler)

        app.logger.setLevel(logging.DEBUG)

