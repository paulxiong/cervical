import logging

class logger():
    def __init__(self, logfile, stdout=False, loglevel=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=loglevel)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        handler = logging.FileHandler(logfile)
        handler.setLevel(loglevel)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        if stdout:
            stdout = logging.StreamHandler()
            stdout.setLevel(loglevel)
            stdout.setFormatter(formatter)
            self.logger.addHandler(stdout)

    def info(self, info):
        self.logger.info(info)
    def warning(self, info):
        self.logger.warning(info)
    def error(self, info):
        self.logger.error(info)
