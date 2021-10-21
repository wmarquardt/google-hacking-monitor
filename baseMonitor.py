import logging
import sys
from colorlog import ColoredFormatter

class BaseMonitor(object):
    debug = False
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, debug=False):
        self.debug = debug
        self.logger = logging.getLogger()
        
        console_handler = logging.StreamHandler()
        
        log_format = '%(asctime)s | %(levelname)s: %(message)s'
        console_handler.setFormatter(ColoredFormatter(log_format))
        
        self.logger.addHandler(console_handler)
        if self.debug:
            self.logger.setLevel(logging.DEBUG)

