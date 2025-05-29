import random
from enum import Enum, auto

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    Filters,
    CallbackContext,
)

import questions
from redis_utils import save_question, get_question


class States(Enum):
    NEW_QUESTION = auto()
    ANSWERING = auto()


def normalize_answer(answer: str) -> str:
    answer = answer.split('.')[0].split('(')[0]
    return answer.strip().lower()


def send_new_question(update: Update, user_id: int) -> States:
    question = random.choice(list(questions.qa_dict.keys()))
    save_question(user_id, question)
    update.message.reply_text(question)
    return States.ANSWERING


def start(update: Update, context: CallbackContext):
    keyboard = [
        ["Новый вопрос", "Сдаться"],
        ["Мой счёт"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Здравствуйте!", reply_markup=reply_markup)
    return States.NEW_QUESTION


def handle_new_question_request(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    return send_new_question(update, user_id)


def handle_give_up(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    question = get_question(user_id)

    if question and (answer := questions.qa_dict.get(question)):
        update.message.reply_text(f"Ответ: {answer}")
    else:
        update.message.reply_text("Вопрос не найден. Нажмите 'Новый вопрос'.")

    return send_new_question(update, user_id)


def handle_solution_attempt(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    question = get_question(user_id)
    correct_answer = questions.qa_dict.get(question)

    user_answer = normalize_answer(update.message.text.strip())
    if user_answer == normalize_answer(correct_answer):
        update.message.reply_text(
            "Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»")
        save_question(user_id, "")
        return States.NEW_QUESTION

    update.message.reply_text("Неправильно… Попробуешь ещё раз?")
    return States.ANSWERING


def handle_score(update: Update, context: CallbackContext):
    update.message.reply_text("Счёт пока не реализован :)")
    return States.NEW_QUESTION


def get_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            States.NEW_QUESTION: [
                MessageHandler(Filters.regex("^Новый вопрос$"),
                               handle_new_question_request),
                MessageHandler(Filters.regex("^Мой счёт$"), handle_score),
            ],
            States.ANSWERING: [
                MessageHandler(Filters.regex("^Сдаться$"), handle_give_up),
                MessageHandler(Filters.regex("^Мой счёт$"),
                               handle_score),
                MessageHandler(
                    Filters.text & ~Filters.regex(
                        "^(Новый вопрос|Сдаться|Мой счёт)$"),
                    handle_solution_attempt,
                ),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
