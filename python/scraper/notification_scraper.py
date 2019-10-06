import re
from datetime import date

import requests
from bs4 import BeautifulSoup

from config.logger import logger
from data.models import Notification

DATE_TAG = 'datetime'
TITLE_CLASS = 'news_title_truncateable'
LINK_START = 'fipu.unipu.hr'


def get_all(link):
    logger.info("Scrapping notifications")

    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    unformatted_dates = soup.findAll('time')
    dates = []
    titles = soup.findAll('div', {'class': TITLE_CLASS})
    links = soup.find_all('a', href=re.compile('/fipu/za_studente/oglasna_ploca'))[4:]

    for index, item in enumerate(unformatted_dates):
        if index % 2 is 0:
            dates.append(item)

    notifications = []

    cur_month = format_small_date(date.today().month)
    cur_day = format_small_date(date.today().day)

    for i in range(len(dates)):
        title = titles[i].contents[0]
        link = links[i]['href']
        post_date = str(dates[i])[16:35]
        month = str(post_date[5:7])
        day = str(post_date[8:10])

        if day != cur_day or month != cur_month:
            break
        notifications.append(Notification(title, '{}{}'.format(LINK_START, link)))

    logger.info("Scraped {} notifications: {}".format(len(notifications), notifications))
    return notifications


def format_small_date(current_date):
    if current_date < 10:
        return '0{}'.format(current_date)
    else:
        return '{}'.format(current_date)
