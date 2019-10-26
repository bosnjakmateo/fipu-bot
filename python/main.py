import threading

from services import notification_classifier, notifier, telegram_bot
from config import logger

notification_classifier.load_data()
threading.Thread(target=notifier.main, daemon=True).start()
threading.Thread(target=logger.main, daemon=True).start()
telegram_bot.start_bot()
