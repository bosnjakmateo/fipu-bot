import os

from models import *

notifiedItems = []
registeredUsers = []

connect(
    host=os.environ['MONGO_URL']
)


def add_user(chat_id):
    if user_registered(chat_id):
        return False

    return Users(chat_id).save()


def remove_user(chat_id):
    if not user_registered(chat_id):
        return False

    return Users.objects(chat_id=chat_id).delete()


def user_registered(chat_id):
    return len(Users.objects(chat_id=chat_id)) is not 0


def users_empty():
    return len(Users.objects) is 0


def item_notified(item):
    return len(Items.objects(title=item.title)) is not 0


def add_notified_item(item):
    Items(item.title).save()


def clean_notified_items():
    Items.objects().delete()
