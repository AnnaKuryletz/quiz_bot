from telegram import Update
from telegram.ext import ContextTypes

def start(update, context):
    update.message.reply_text("Здравствуйте")

def echo(update, context):
    update.message.reply_text(update.message.text)