class BaseMonitor(object):
    def print_debug(self, message):
        if self.debug: print(message)
