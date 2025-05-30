import os
from dotenv import load_dotenv
from telegram.ext import Updater

from handlers_for_tg import get_conversation_handler
from questions import load_questions_from_file
from redis_connect import connect_to_db


def main():
    load_dotenv()
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    questions = load_questions_from_file("quiz-questions/1vs1200.txt")
    redis_conn = connect_to_db()

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(get_conversation_handler(questions, redis_conn))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
