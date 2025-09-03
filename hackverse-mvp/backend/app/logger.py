import logging
from logging.handlers import RotatingFileHandler

LOGFILE = 'hackverse.log'

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler = RotatingFileHandler(LOGFILE, maxBytes=10*1024*1024, backupCount=5)
handler.setFormatter(formatter)

logger = logging.getLogger('hackverse')
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(handler)

# helper
def get_logger(name: str = None):
    return logging.getLogger(name or 'hackverse')
