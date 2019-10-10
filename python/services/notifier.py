import time

import schedule

from config.logger import logger
from database import notifications_db
from database import users_db
from scraper import notification_scraper
from services import notification_classifier, telegram_bot


def main():
    schedule.every().hour.at(":00").do(job)
    schedule.every().hour.at(":30").do(job)
    schedule.every().day.at("02:00").do(notifications_db.delete_all)

    logger.info("Service started")

    while True:
        schedule.run_pending()
        time.sleep(1)


def job():
    if users_db.users_empty():
        logger.info("No users in db")
        return

    notifications = notification_scraper.get_all('https://fipu.unipu.hr/fipu/za_studente/oglasna_ploca')

    filtered_items = filter_notifications(notifications)

    if not filtered_items:
        logger.info("No new notifications. Ending job")
        return

    classified_items = notification_classifier.classify(filtered_items)

    users = users_db.get_all()

    logger.info("Sending messages to {} users".format(len(users)))
    for user in users:
        users_items = get_items(classified_items, user.year)
        if len(users_items) is 0:
            logger.info("User ({}) has not items, skipping user".format(user.chat_id))
            continue

        logger.info("User ({}) notifications: {}".format(user.chat_id, users_items))

        content = format_content(users_items)

        logger.info("Sending message to user ({})".format(user.chat_id))
        telegram_bot.send_message("Nove obavijesti: {}".format(content), user.chat_id)

    logger.info("Job ended")


def filter_notifications(notifications):
    new_notifications = []
    logger.info("Filtering notifications")

    if not notifications:
        return []

    for item in notifications:
        if not notifications_db.notified(item):
            new_notifications.append(item)
            notifications_db.add(item)

    logger.info("Filtered {} notifications: {}".format(len(new_notifications), new_notifications))
    return new_notifications


def format_content(notifications):
    formatted_content = map(lambda item: '[{}]({})'.format(remove_brackets(item.title), item.link), notifications)
    return '\n'.join(formatted_content)


def remove_brackets(title):
    return title.replace('[', '').replace(']', '')


def get_items(classified_items, year):
    items = [*classified_items[0]]
    years = [1, 2, 3, 4, 5]

    if year is 0:
        for year in years:
            items = items + classified_items[year]

        return items
    else:
        return items + classified_items[year]
