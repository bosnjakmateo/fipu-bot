import threading

from services import notification_classifier, notifier, telegram_bot

notification_classifier.load_data()
threading.Thread(target=notifier.main, daemon=True).start()
telegram_bot.start_bot()
