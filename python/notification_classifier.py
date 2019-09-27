from models import Subject
from scraper import subject_scraper
import re


PREDDIPLOMSKI = 'https://fipu.unipu.hr/fipu/studijski_programi/preddiplomski_sveucilisni_studij_informatika'
DIPLOMSKI = 'https://fipu.unipu.hr/fipu/studijski_programi/preddiplomski_sveucilisni_studij_informatika'

classified_subjects = []


def classify_items(items):
    classified_items = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

    for item in items:
        year = get_year(item)
        classified_items[year].append(item)

    return classified_items


def load_data():
    global classified_subjects
    classified_subjects = []

    get_subjects(PREDDIPLOMSKI, False)
    get_subjects(DIPLOMSKI, True)


def get_subjects(link, diplomski):
    items = subject_scraper.get_items(link)

    semester = ''

    for item in items:
        if 'semestar' in item:
            semester = item
            continue

        classified_subjects.append(Subject(item, extract_year(semester, diplomski)))


def get_year(item):
    for subject in classified_subjects:
        if subject.name in item.title:
            return subject.year

    return 0


def extract_year(semester, diplomski):
    year = re.findall(''', \d''', semester)
    year = int(year[0][-1:])

    if diplomski:
        year = year + 3

    return year
