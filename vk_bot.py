import os
import argparse
from dotenv import load_dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from handlers_for_vk import handle_message
from questions import load_questions_from_file
from redis_connect import connect_to_db


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Запуск VK бота-викторины")
    parser.add_argument(
        "--questions",
        help="Путь к файлу с вопросами",
        default=os.getenv("QUESTIONS_FILE", "quiz-questions/1vs1200.txt")
    )
    args = parser.parse_args()

    questions = load_questions_from_file(args.questions)

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

    vk_token = os.environ["VK_API_KEY"]
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, vk_api, questions, redis_conn)


if __name__ == "__main__":
    main()
