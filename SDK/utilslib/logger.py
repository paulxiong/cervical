import logging

class logger():
    def __init__(self, logfile, loglevel=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=loglevel)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.handler = None
        self.stdouthandler = None

        if logfile is not None:
            self.handler = logging.FileHandler(logfile)
            self.handler.setLevel(loglevel)
            self.handler.setFormatter(formatter)
            self.logger.addHandler(self.handler)

        self.stdouthandler = logging.StreamHandler()
        self.stdouthandler.setLevel(loglevel)
        self.stdouthandler.setFormatter(formatter)
        self.logger.addHandler(self.stdouthandler)

    def info(self, info):
        self.logger.info(info)

    def warning(self, info):
        self.logger.warning(info)

    def error(self, info):
        self.logger.error(info)

    def __del__(self):
        if self.handler is not None:
            self.logger.removeHandler(self.handler)
            self.handler = None
        if self.stdouthandler is not None:
            self.logger.removeHandler(self.stdouthandler)
            self.stdouthandler = None
        self.logger = None
