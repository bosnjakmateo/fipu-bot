import time

import schedule

import notification_classifier
import telegram_bot
from logger import *
from database import notifications_db
from database import users_db
from scraper import notification_scraper


def filter_notified_items(items):
    new_items = []
    logger.info("Filtering notified notifications")

    if not items:
        return []

    for item in items:
        if not notifications_db.item_notified(item):
            new_items.append(item)
            notifications_db.add_notified_item(item)

    logger.info("Filtered {} notifications\n{}".format(len(new_items), new_items))
    return new_items


def format_content(items):
    formatted_items = map(lambda item: '[{}]({})'.format(remove_brackets(item.title), item.link), items)
    return '\n'.join(formatted_items)


def remove_brackets(title):
    return title.replace('[', '').replace(']', '')


def job():
    logger.info("Job started")

    if users_db.users_empty():
        logger.info("No users in db")
        return

    items = notification_scraper.get_items('https://fipu.unipu.hr/fipu/za_studente/oglasna_ploca')

    if not items:
        logger.info("No new notifications. Ending job")
        return

    filtered_items = filter_notified_items(items)
    classified_items = notification_classifier.classify_items(filtered_items)

    users = users_db.get_users()

    logger.info("Sending messages to {} users".format(len(users)))
    for user in users:
        users_items = get_items(classified_items, user['year'])
        if len(users_items) is 0:
            logger.info("User ({}) has not items, skipping user".format(user['chat_id']))
            continue

        logger.info("User ({}) notifications {}".format(user['chat_id'], users_items))

        content = format_content(users_items)

        logger.info("Sending message to user ({})".format(user['chat_id']))
        telegram_bot.send_message("Nove obavijesti: {}".format(content), user['chat_id'])

    logger.info("Job ended")


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

logger.info("Service started")

while True:
    schedule.run_pending()
    time.sleep(1)
