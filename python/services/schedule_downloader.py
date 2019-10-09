from io import BytesIO

import requests
from pdf2image import convert_from_bytes

from config.logger import logger

schedules_map = {
    'p1': 'Informatika_-_1._semestar.pdf',
    'p2': 'Informatika_-_2._semestar.pdf',
    'p3': 'Informatika_-_3._semestar.pdf',
    'p4': 'Informatika_-_4._semestar.pdf',
    'p5': 'Informatika_-_5._semestar.pdf',
    'p6': 'Informatika_-_6._semestar.pdf',
    'd1': 'Diplomski_studij_Informatika_-_1._semestar.pdf',
    'd2': 'Diplomski_studij_Informatika_-_2._semestar.pdf',
    'd3': 'Diplomski_studij_Informatika_-_3._semestar.pdf',
    'd4': 'Diplomski_studij_Informatika_-_4._semestar.pdf',
    'dn1': 'Diplomski_studij_Informatika_-_nastavni_smjer_-_1._semestar.pdf',
    'dn2': 'Diplomski_studij_Informatika_-_nastavni_smjer_-_2._semestar.pdf',
    'dn3': 'Diplomski_studij_Informatika_-_nastavni_smjer_-_3._semestar.pdf',
    'dn4': 'Diplomski_studij_Informatika_-_nastavni_smjer_-_4._semestar.pdf',
}

BASE_LINK = 'https://fipu.unipu.hr/_download/repository/'


def get_schedule(semester):
    url = '{}{}'.format(BASE_LINK, schedules_map[semester])
    r = requests.get(url, stream=True)

    try:
        images = convert_from_bytes(r.content, fmt="png")
        bio = BytesIO()

        for image in images:
            image.save(bio, "png")
            bio.seek(0)

        return bio

    except Exception:
        logger.error("Error during schedule download")
        return {}
