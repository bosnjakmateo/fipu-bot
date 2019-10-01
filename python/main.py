import time

import schedule

import notification_classifier
import telegram_bot
from database import notifications_db
from database import users_db
from scraper import notification_scraper


def filter_notified_items(items):
    new_items = []

    for item in items:
        if not notifications_db.item_notified(item):
            new_items.append(item)
            notifications_db.add_notified_item(item)

    return new_items


def format_content(items):
    formatted_items = map(lambda item: '[{}]({})'.format(remove_brackets(item.title), item.link), items)
    return '\n'.join(formatted_items)


def remove_brackets(title):
    return title.replace('[', '').replace(']', '')


def job():
    if users_db.users_empty():
        return

    items = notification_scraper.get_items('https://fipu.unipu.hr/fipu/za_studente/oglasna_ploca')

    filtered_items = filter_notified_items(items)
    classified_items = notification_classifier.classify_items(filtered_items)

    users = users_db.get_users()

    for user in users:
        users_items = get_items(classified_items, user['year'])

        if len(users_items) is 0:
            continue

        content = format_content(users_items)
        telegram_bot.send_message("Nove obavijesti:\n{}".format(content), int(user['chat_id']))


def get_items(classified_items, year):
    items = [*classified_items[0]]
    years = [1, 2, 3, 4, 5]

    if year is 0:
        for year in years:
            items = items + classified_items[year]

        return items
    else:
        return items + classified_items[year]


telegram_bot.start_bot()
notification_classifier.load_data()

schedule.every().hour.at(":00").do(job)
schedule.every().hour.at(":30").do(job)
schedule.every().day.at("02:00").do(notifications_db.clean_notified_items)

while True:
    schedule.run_pending()
    time.sleep(1)
