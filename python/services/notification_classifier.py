import re

from config.logger import *
from data.models import Subject
from scraper import subject_scraper

PREDDIPLOMSKI = 'https://fipu.unipu.hr/fipu/studijski_programi/preddiplomski_sveucilisni_studij_informatika'
DIPLOMSKI = 'https://fipu.unipu.hr/fipu/studijski_programi/preddiplomski_sveucilisni_studij_informatika'

classified_subjects = []


def classify(notifications):
    classified_notifications = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
    logger.info("Classifying notifications {}".format(notifications))

    for notification in notifications:
        year = get_year(notification)
        classified_notifications[year].append(notification)

    logger.info("Classified notifications {}".format(classified_notifications))
    return classified_notifications


def load_data():
    logger.info("Starting subject loading")

    global classified_subjects
    classified_subjects = []

    get_subjects(PREDDIPLOMSKI, False)
    get_subjects(DIPLOMSKI, True)

    logger.info("Subject loading finished")


def get_subjects(link, graduate):
    global classified_subjects
    items = subject_scraper.get_all(link)

    semester = ''

    for item in items:
        if 'semestar'.lower() in item.lower():
            semester = item
            continue

        classified_subjects.append(Subject(item, extract_year(semester, graduate)))


def get_year(item):
    for subject in classified_subjects:
        if subject.name in item.title:
            return subject.year

    return 0


def extract_year(semester, graduate):
    year = re.findall(''', \d''', semester)
    year = int(year[0][-1:])

    if graduate:
        year = year + 3

    return year
