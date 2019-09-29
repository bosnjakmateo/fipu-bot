import os

from pymongo import MongoClient

client = MongoClient(host=os.environ['MONGO_URL'])
users_collection = client['fipu-bot']['users']


def add_user(chat_id):
    if user_registered(chat_id):
        return False

    return users_collection.insert_one({'chat_id': chat_id, 'year': 0})


def get_user(chat_id):
    return users_collection.find_one({'chat_id': chat_id})


def get_users():
    users = []

    cursor = users_collection.find({})

    for document in cursor:
        users.append(document)

    return users


def remove_user(chat_id):
    if not user_registered(chat_id):
        return False

    return users_collection.delete_one({'chat_id': chat_id})


def update_year(chat_id, year):
    users_collection.update_one({'chat_id': chat_id}, {'$set': {'chat_id': chat_id, 'year': year}})


def user_registered(chat_id):
    return users_collection.find({'chat_id': chat_id}).count() > 0


def users_empty():
    return users_collection.find({}).count() == 0
