import os

from pymongo import MongoClient

from config.logger import logger

client = MongoClient(host=os.environ['MONGO_URL'])
notifications = client['fipu-bot']['notifications']


def notified(item):
    return notifications.find({'title': item.title}).count() > 0


def add(item):
    notifications.insert_one({'title': item.title})


def delete_all():
    logger.info("Deleting notifications")
    notifications.delete_many({})
    logger.info("Notifications deleted")
