from os.path import join, abspath, dirname
from ConfigParser import SafeConfigParser


class CvConfig(object):
    def get(self, item, key):
        return self.parser.get(item, key)

    def __init__(self):
        config_file = join(dirname(dirname(dirname(abspath(__file__)))),
                           'configs', 'dev.config.ini')
        self.parser = SafeConfigParser()
        self.parser.read(config_file)

