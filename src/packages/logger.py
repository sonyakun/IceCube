import logging

class log:

    def getlogger(self):
        self.logger = logging.getLogger('discord')
        if not self.logger.hasHandlers():
            handler = logging.FileHandler(filename='log/icecube.log', encoding='utf-8', mode='w')
            handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
            self.logger.addHandler(handler)
        return self.logger