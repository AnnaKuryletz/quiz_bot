from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
import random
import questions
from redis_utils import save_question, get_question


def echo(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    user_id = update.effective_user.id

    if text == "Новый вопрос":
        question = random.choice(list(questions.qa_dict.keys()))
        save_question(user_id, question)
        update.message.reply_text(question)
    elif text == "Сдаться":
        question = get_question(user_id)
        if question:
            answer = questions.qa_dict.get(question)
            update.message.reply_text(f"Ответ: {answer}")
        else:
            update.message.reply_text(
                "Вопрос не найден. Нажмите 'Новый вопрос'.")


def start(update: Update, context: CallbackContext):
    keyboard = [
        ["Новый вопрос", "Сдаться"],
        ["Мой счёт"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text(
        "Здравствуйте!", reply_markup=reply_markup)
