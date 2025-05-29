from dotenv import load_dotenv
import os
from telegram.ext import Updater
from handlers import get_conversation_handler


def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(get_conversation_handler())
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
