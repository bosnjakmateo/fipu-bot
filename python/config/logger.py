import logging

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('output.log', 'w', 'utf-8')],
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
)

logger = logging
