import configparser
import telebot
from repository.users import get_users
from repository.users import create_user

config = configparser.ConfigParser()
config.read('config.ini')

token = config['Telegram']['token']

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
    markup.add(telebot.types.KeyboardButton('Выбрать время для запроса параметров'))
    markup.add(telebot.types.KeyboardButton('Получить отчетность по заданному периоду'))
    bot.send_message(message.chat.id, "Теперь тебе доступен функционал бота", reply_markup=markup)


bot.polling(none_stop=True)
