import logging

class logger():
    def __init__(self, jobId, jobdir):
        self.jid = jobId
        self.logfile = jobdir + '/' + jobId + '.log'
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level = logging.INFO)
        self.handler = logging.FileHandler(self.logfile)
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
    def info(self, info):
        self.logger.info(info)
    def warning(self, info):
        self.logger.warning(info)
