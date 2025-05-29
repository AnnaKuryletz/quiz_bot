import os

from dotenv import load_dotenv
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

from handlers_for_vk import handle_message


def main():
    load_dotenv()
    vk_token = os.getenv("VK_API_KEY")
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, vk_api)


if __name__ == "__main__":
    main()
