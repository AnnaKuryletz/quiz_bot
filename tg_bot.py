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

    redis_host = os.environ["REDIS_DATABASE_URL"]
    redis_port = int(os.environ["REDIS_PORT"])
    redis_user = os.getenv("REDIS_USERNAME", "default")
    redis_password = os.environ["REDIS_PASSWORD"]

    redis_conn = connect_to_db(
        host=redis_host,
        port=redis_port,
        username=redis_user,
        password=redis_password,
    )

    questions = load_questions_from_file(args.questions)

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(get_conversation_handler(questions, redis_conn))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
