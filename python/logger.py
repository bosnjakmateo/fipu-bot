import logging

logging.basicConfig(
    level=logging.INFO,
    filename='out.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
)

logger = logging
