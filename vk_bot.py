import os

from dotenv import load_dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from handlers_for_vk import handle_message
from questions import load_questions_from_file
from redis_connect import connect_to_db


def main():
    load_dotenv()
    questions = load_questions_from_file("quiz-questions/1vs1200.txt")
    redis_conn = connect_to_db()

    vk_token = os.environ["VK_API_KEY"]
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, vk_api, questions, redis_conn)


if __name__ == "__main__":
    main()
