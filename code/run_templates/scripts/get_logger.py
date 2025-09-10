import logging
import sys

logger = logging.getLogger("CSM display")
formatter = logging.Formatter('%(message)s')
std_handler = logging.StreamHandler(sys.stdout)
std_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(std_handler)
