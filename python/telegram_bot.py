from telegram.ext import Updater, CommandHandler
import database
import os

updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=True)
dispatcher = updater.dispatcher


def send_message(message, chat_id):
    dispatcher.bot.send_message(parse_mode='Markdown', chat_id=chat_id, text=message, disable_web_page_preview=True)


def send_welcome(update, context):
    context.bot.send_message(update.message.chat_id,
                             "Ja sam FIPU bot, poslat ću ti svaku novu obavijesti sa oglasne ploče.\n"
                             "Pošalji '/register' za primanje obavijesti, ili '/unregister' da ih prestaneš dobivati")


def register(update, context):
    registered = database.add_user(update.message.chat.id)

    if registered:
        context.bot.send_message(chat_id=update.message.chat_id, text="Registracija uspješna!")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Već si registriran/a!")


def unregister(update, context):
    removed = database.remove_user(update.message.chat.id)

    if removed:
        context.bot.send_message(chat_id=update.message.chat_id, text="Nisi više registriran/a!")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Već si se odjavio/la od dobivanja obavijesti!")


dispatcher.add_handler(CommandHandler('start', send_welcome))
dispatcher.add_handler(CommandHandler('help', send_welcome))
dispatcher.add_handler(CommandHandler('register', register))
dispatcher.add_handler(CommandHandler('unregister', unregister))


def start_bot():
    updater.start_polling()
