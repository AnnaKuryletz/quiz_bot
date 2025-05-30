import json
import random

from redis_utils import save_question, get_question
from quiz_utils import normalize_answer


def send_keyboard(vk_api, user_id, message):
    keyboard = {
        "one_time": False,
        "buttons": [
            [{"action": {"type": "text", "label": "Новый вопрос"}, "color": "primary"}],
            [{"action": {"type": "text", "label": "Сдаться"}, "color": "default"}],
            [{"action": {"type": "text", "label": "Мой счёт"}, "color": "default"}],
        ]
    }
    vk_api.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 100000),
        keyboard=json.dumps(keyboard)
    )


def handle_message(event, vk_api, questions: dict, redis_conn):
    user_id = event.user_id
    text = event.text.strip()

    if text == "/start":
        send_keyboard(vk_api, user_id, "Здравствуйте!")
    elif text == "Новый вопрос":
        question = random.choice(list(questions.keys()))
        save_question(redis_conn, user_id, question, "vk")
        vk_api.messages.send(
            user_id=user_id,
            message=question,
            random_id=random.randint(1, 100000)
        )
    elif text == "Сдаться":
        question = get_question(redis_conn, user_id, "vk")
        if question:
            answer = questions.get(question)
            vk_api.messages.send(
                user_id=user_id,
                message=f"Ответ: {answer}",
                random_id=random.randint(1, 100000)
            )
        else:
            vk_api.messages.send(
                user_id=user_id,
                message="Вопрос не найден. Нажмите 'Новый вопрос'.",
                random_id=random.randint(1, 100000)
            )
        new_question = random.choice(list(questions.keys()))
        save_question(redis_conn, user_id, question, "vk")
        vk_api.messages.send(
            user_id=user_id,
            message=f"Новый вопрос: {new_question}",
            random_id=random.randint(1, 100000)
        )
    elif text == "Мой счёт":
        vk_api.messages.send(
            user_id=user_id,
            message="Счёт пока не реализован :)",
            random_id=random.randint(1, 100000)
        )
    else:
        question = get_question(redis_conn, user_id, "vk")
        correct_answer = questions.get(question)
        if not correct_answer:
            vk_api.messages.send(
                user_id=user_id,
                message="Ошибка: вопрос не найден.",
                random_id=random.randint(1, 100000)
            )
            return
        if normalize_answer(text) == normalize_answer(correct_answer):
            vk_api.messages.send(
                user_id=user_id,
                message="Правильно! Поздравляю! Нажми «Новый вопрос» для следующего.",
                random_id=random.randint(1, 100000)
            )
            save_question(redis_conn, user_id, "vk")
        else:
            vk_api.messages.send(
                user_id=user_id,
                message="Неправильно… Попробуешь ещё раз?",
                random_id=random.randint(1, 100000)
            )
