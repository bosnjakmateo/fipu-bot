import os

from pymongo import MongoClient
from logger import *

client = MongoClient(host=os.environ['MONGO_URL'])
notifications = client['fipu-bot']['notifications']


def item_notified(item):
    return notifications.find({'title': item.title}).count() > 0


def add_notified_item(item):
    notifications.insert_one({'title': item.title})


def clean_notified_items():
    logger.info("Starting to clean notified notifications")
    notifications.delete_many({})
    logger.info("Notified notifications cleaned successfully")
