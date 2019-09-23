from mongoengine import *


class Users(Document):
    chat_id = LongField(required=True)


class Items(Document):
    title = StringField(required=True)


class Item:
    def __init__(self, title, link):
        self.title = title
        self.link = link
