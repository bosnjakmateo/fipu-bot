from telegram.ext import Updater, CommandHandler
from database import users_db
from data.messages import *
from logger import *
import os

updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=True)
dispatcher = updater.dispatcher

year_descriptions = {
    0: "0 - sve obavijesti",
    1: "1 - 1. preddiplomska",
    2: "2 - 2. preddiplomska",
    3: "3 - 3. preddiplomska",
    4: "4 - 1. diplomska",
    5: "5 - 2. diplomska"
}


def send_message(message, chat_id):
    dispatcher.bot.send_message(parse_mode='Markdown', chat_id=int(chat_id), text=message, disable_web_page_preview=True)


def send_welcome(update, context):
    context.bot.send_message(update.message.chat_id, START_MESSAGE)


def register(update, context):
    registered = users_db.add_user(update.message.chat.id)

    if registered:
        context.bot.send_message(chat_id=update.message.chat_id, text=REGISTER_SUCCESS)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=ALREADY_REGISTERED)


def unregister(update, context):
    removed = users_db.remove_user(update.message.chat.id)

    if removed:
        context.bot.send_message(chat_id=update.message.chat_id, text=UNREGISTER_SUCCESS)
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text=ALREADY_UNREGISTER)


def update_year(update, context):
    registered = users_db.add_user(update.message.chat.id)

    if registered:
        context.bot.send_message(chat_id=update.message.chat_id, text=NEED_TO_BE_REGISTERED)
        return

    try:
        year = int(context.args[0])
    except ValueError:
        context.bot.send_message(chat_id=update.message.chat_id, text=UPDATE_YEAR_PARAMETER_INVALID)
        return

    if year > 5:
        context.bot.send_message(chat_id=update.message.chat_id, text=UPDATE_YEAR_EXCEEDED)
        return

    users_db.update_year(update.message.chat.id, year)

    context.bot.send_message(chat_id=update.message.chat_id, text=UPDATE_YEAR_SUCCESS.format(year_descriptions[year]))


def get_all_commands(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=ALL_COMMANDS)


def get_info(update, context):
    registered = users_db.user_registered(update.message.chat.id)

    if not registered:
        context.bot.send_message(chat_id=update.message.chat_id, text=NEED_TO_BE_REGISTERED)
        return

    user = users_db.get_user(update.message.chat.id)

    context.bot.send_message(chat_id=update.message.chat_id, text=INFO.format(year_descriptions[int(user['year'])]))


dispatcher.add_handler(CommandHandler('start', send_welcome))
dispatcher.add_handler(CommandHandler('registracija', register))
dispatcher.add_handler(CommandHandler('odjava', unregister))
dispatcher.add_handler(CommandHandler('godina', update_year, pass_args=True))
dispatcher.add_handler(CommandHandler('info', get_info))
dispatcher.add_handler(CommandHandler('pomoc', get_all_commands))


def start_bot():
    updater.start_polling()
    logger.info("Bot polling started")
    updater.idle()
