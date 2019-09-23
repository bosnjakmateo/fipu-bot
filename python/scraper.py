from bs4 import BeautifulSoup
from datetime import date
from models import Item
import requests
import re


DATE_TAG = 'datetime'
TITLE_CLASS = 'news_title_truncateable'
LINK_START = 'fipu.unipu.hr'


def format_small_date(current_date):
    if current_date < 10:
        return '0{}'.format(current_date)
    else:
        return '{}'.format(current_date)


def get_items(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    unformatted_dates = soup.findAll('time')
    dates = []
    titles = soup.findAll('div', {'class': TITLE_CLASS})
    links = soup.find_all('a', href=re.compile('/fipu/za_studente/oglasna_ploca'))[4:]

    for index, item in enumerate(unformatted_dates):
        if index % 2 is 0:
            dates.append(item)

    items = []

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

        items.append(Item(title, '{}{}'.format(LINK_START, link)))

    return items
