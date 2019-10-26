import logging
import time

import schedule

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('output.log', 'w', 'utf-8')],
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%y %H:%M:%S'
)

logger = logging


def clean_log():
    file = open("output.log", "w")
    file.close()


def main():
    schedule.every(3).days.do(clean_log)

    logger.info("Log file cleaned")

    while True:
        schedule.run_pending()
        time.sleep(1)
