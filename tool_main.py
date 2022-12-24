from di_container import DIContainer
from commons import Commons
import datetime
from pathlib import Path


class ToolMain:
    def __init__(self):
        self.container = DIContainer()
        self.conf = self.container.conf
        self.logger = self.container.logger
        self.today = datetime.date.today()

    def execute(self):
        self.logger.debug(self.container)
        self.logger.debug(self.conf)
        self.logger.debug(self.logger)
        self.logger.debug(self.today)
