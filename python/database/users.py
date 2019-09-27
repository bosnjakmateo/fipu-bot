import os

from models import *

connect(
    host=os.environ['MONGO_URL']
)


def add_user(chat_id):
    if user_registered(chat_id):
        return False

    return Users(chat_id, "0").save()


def get_user(chat_id):
    return Users.objects(chat_id=chat_id).first()


def remove_user(chat_id):
    if not user_registered(chat_id):
        return False

    return Users.objects(chat_id=chat_id).delete()


def update_year(chat_id, year):
    user = Users.objects(chat_id=chat_id).first()
    user.year = str(year)
    user.save()


def user_registered(chat_id):
    return len(Users.objects(chat_id=chat_id)) is not 0


def users_empty():
    return len(Users.objects) is 0
