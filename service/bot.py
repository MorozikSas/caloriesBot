import telebot
from repository.users import get_users
from repository.users import create_user
from mapper.buttonMapper import get_handler
from external.deepinfra import createRequest
from config import TelegramConfig
from config import Buttons

token = TelegramConfig.TOKEN
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"User with {message.chat.id} is started to use bot")
    user = get_users(message.chat.id)
    if user is None:
        print(f'Create new user {message.chat.id}, {message.chat.first_name}')
        create_user(message.chat.id, message.chat.first_name)
        bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}. Теперь ты зарегистрирован и тебе доступен функционал бота')
    else:
        userName = user[0][1]
        bot.send_message(message.chat.id, f'Привет, {userName}')
    default_buttons(message)

def default_buttons(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton(Buttons.takeTime))
    markup.add(telebot.types.KeyboardButton(Buttons.getData))
    bot.send_message(message.chat.id, "Теперь тебе доступен функционал бота", reply_markup=markup)

@bot.message_handler(commands=['ai'])
def handle_ai(message):
    mess = 'Привет. Это тест. Напиши "Валера"'
    data = createRequest(mess)
    bot.send_message(message.chat.id, f"Оракул ответил:{data}")

@bot.message_handler()
def handle_message(message):
    print(f"client {message.chat.id}, put {message.text}")
    handler_name = get_handler(message.text)
    handler = globals().get(handler_name)
    if handler is not None:
        handler(message)
    else:
        bot.send_message(message.chat.id, "Выбери из предложенного, не пиши сам")
        default_buttons(message)

def takeTime(message):
    bot.send_message(message.chat.id, "Вы выбрали время для запроса параметров")

def getData(message):
    bot.send_message(message.chat.id, "Вы получаете отчетность по заданному периоду")


# @bot.message_handler(commands=['schedule'])
# def handle_ai(message):
#     bot.send_message(message.chat.id, f"Введи дату в формате ")


bot.polling(none_stop=True)
