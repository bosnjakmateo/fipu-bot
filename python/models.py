from mongoengine import *


class Users(Document):
    chat_id = LongField(required=True)
    year = IntField(required=True)


class Items(Document):
    title = StringField(required=True)


class Notification:
    def __init__(self, title, link):
        self.title = title
        self.link = link


class Subject:
    def __init__(self, name, year):
        self.name = name
        self.year = year
