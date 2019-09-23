import time
import schedule
import scraper
import telegram_bot
import database


def filter_notified_items(items):
    new_items = []

    for item in items:
        if not database.item_notified(item):
            new_items.append(item)
            database.add_notified_item(item)

    return new_items


def format_content(items):
    formatted_items = map(lambda item: '[{}]({})'.format(item.title, item.link), items)
    return '\n'.join(formatted_items)


def job():
    if database.users_empty():
        return

    items = scraper.get_items('https://fipu.unipu.hr/fipu/za_studente/oglasna_ploca')

    filtered_items = filter_notified_items(items)

    if filtered_items:
        content = format_content(filtered_items)

        for user in database.Users.objects:
            telegram_bot.send_message("Nove obavijesti:\n{}".format(content), user['chat_id'])


telegram_bot.start_bot()

schedule.every().hour.at(":00").do(job)
schedule.every().hour.at(":30").do(job)
schedule.every().day.at("02:00").do(database.clean_notified_items)

while True:
    schedule.run_pending()
    time.sleep(1)
