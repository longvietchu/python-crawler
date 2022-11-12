import datetime
import logging
import os

# logger = logging.getLogger('crawl-data')
# logger.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', filename='logs/logs-{}.log'.format(n), level=logging.INFO)
# create the logging instance for logging to file only
logger = logging.getLogger('SmartfileTest')

if not os.path.exists('logs'):
    os.makedirs('logs')

n = datetime.datetime.now().strftime('%Y-%m-%d')
log_dir = 'logs/logs-{}.log'.format(n)
file_logger = logging.FileHandler(log_dir)

LOG_FORMAT = '[%(asctime)s] - [%(levelname)s] - %(message)s'
file_logger_format = logging.Formatter(LOG_FORMAT)
file_logger.setFormatter(file_logger_format)

logger.addHandler(file_logger)
logger.setLevel(logging.DEBUG)