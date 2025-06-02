import os
import argparse
from dotenv import load_dotenv
from telegram.ext import Updater

from handlers_for_tg import get_conversation_handler
from questions import load_questions_from_file
from redis_connect import connect_to_db


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Запуск Telegram бота-викторины")
    parser.add_argument(
        "--questions",
        help="Путь к файлу с вопросами",
        default=os.getenv("QUESTIONS_FILE", "quiz-questions/1vs1200.txt")
    )
    args = parser.parse_args()

    token = os.environ["TELEGRAM_BOT_TOKEN"]
    questions = load_questions_from_file(args.questions)
    redis_conn = connect_to_db()

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(get_conversation_handler(questions, redis_conn))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
