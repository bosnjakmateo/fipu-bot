import os

from models import *

connect(
    host=os.environ['MONGO_URL']
)


def item_notified(item):
    return len(Items.objects(title=item.title)) is not 0


def add_notified_item(item):
    Items(item.title).save()


def clean_notified_items():
    Items.objects().delete()
