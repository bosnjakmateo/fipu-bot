import os

from pymongo import MongoClient

client = MongoClient(host=os.environ['MONGO_URL'])
notifications = client['fipu-bot']['notifications']


def item_notified(item):
    return notifications.find({'title': item.title}).count() > 0


def add_notified_item(item):
    notifications.insert_one({'title': item.title})


def clean_notified_items():
    notifications.delete_many({})
