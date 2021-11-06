import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from class_ofd import OfdClient
from datetime import datetime
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.proxy_url,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    print('Вызови /start')
    update.message.reply_text('Привет, чувачок! Хочешь активировать подписку?')

    return 'start_registration'


def start_registration(update, context):
    user_talk = update.message.text
    if user_talk == 'Да' or user_talk == 'да':
        update.message.reply_text('Введите регистрационный номер')
        return 'get_reg_number'
    elif user_talk == 'Нет' or user_talk == 'нет':
        update.message.reply_text('Минус премия, другалик')
        return cancel_handler(update, context)
    update.message.reply_text('Необходимо ввести "Да" или "Нет"!')
    return 'start_registration'


def get_reg_number(update, context):
    reg_number = update.message.text
    print(reg_number)

    if len(reg_number) != 16:
        update.message.reply_text('РНМ должен быть не менее 16 символов')
        return cancel_handler(update, context)

    context.user_data['reg_number'] = reg_number
    update.message.reply_text('Введите промо-код')

    return 'get_activation_code'


def get_activation_code(update, context):
    activation_code = update.message.text
    print(activation_code)
    context.user_data['activation_code'] = activation_code
    return registrate_activate(update, context)

def registrate_activate(update, context):
    client = OfdClient(login=settings.login, password=settings.password)
    result_activation = client.activate_subscription(
        reg_number=context.user_data.get('reg_number'),
        code_activate=context.user_data.get('activation_code')
    )
    print(result_activation)
    date_activation = result_activation.get('to')
    if date_activation is None:
        update.message.reply_text(result_activation.get('message'))
    else:
        date_activation_to = datetime.fromtimestamp(date_activation // 1000)
        update.message.reply_text(date_activation_to.strftime("%m/%d/%Y"))
        print(date_activation_to.strftime("%d/%m/%Y"))
    return cancel_handler(update, context)


def cancel_handler(update, context):
    update.message.reply_text('Отмена. Для начала нажмите /start')
    return ConversationHandler.END


def main():
    bot = Updater(settings.API_KEY, use_context=True)
    logging.info('Бот начал работу')
    dp = bot.dispatcher


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', greet_user)],
        states={'start_registration': [MessageHandler(Filters.all, start_registration, pass_user_data=True)],
        'get_reg_number': [MessageHandler(Filters.all, get_reg_number, pass_user_data=True)],
        'get_activation_code': [MessageHandler(Filters.all, get_activation_code, pass_user_data=True)]},
        fallbacks=[CommandHandler('cancel', cancel_handler)]
    )

    dp.add_handler(conv_handler)

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
