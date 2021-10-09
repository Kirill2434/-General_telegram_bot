from datetime import datetime
from telegram import update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from telegram.utils.request import Request
import settings 
import logging

logging.basicConfig(filename='bot.log', level=logging.INFO)


def greet_user(update, context):
    print("Вызван /start")
    update.message.reply_text("Здравствуй, пользователь!")  

def check_connectin(update, context):
    print("Отправляем запрос во Falsk")
    resp = requests.post(url='https://1bc1-2a00-1370-8123-c463-98d7-b65c-f0a0-f535.ngrok.io')
    print(resp.text)
    update.message.reply_text(resp.text)


def get_info_lmfc(update, context):
    print("Получаем информацию с сайта")
    info = requests.post(url='http://1bc1-2a00-1370-8123-c463-98d7-b65c-f0a0-f535.ngrok.io/parser/infoLMFC', json={'url': 'https://www.fclm.ru/ru/season/calendar#1/21/0/matches'})
    print(info.json())
    update.message.reply_text(info.json())


def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def main():
    bot = Updater(settings.API_KEY, use_context=True)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("Check", check_connectin))
    dp.add_handler(CommandHandler('Check_info', get_info_lmfc))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Бот стартовал")
    bot.start_polling()
    bot.idle()



if __name__ == "__main__":
    main()