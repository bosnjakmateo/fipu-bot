class User:
    def __init__(self, chat_id, year):
        self.chat_id = chat_id
        self.year = year


class Notification:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class Subject:
    def __init__(self, name, year):
        self.name = name
        self.year = year
