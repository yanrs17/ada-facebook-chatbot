import logging
import os
import sys

from .scrapers.reddit import Reddit

class NullHandler(logging.Handler):

    def emit(self, record):
        pass

logging.getLogger('uoftscrapers').addHandler(NullHandler())
