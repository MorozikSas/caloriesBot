import configparser
import telebot
from repository.users import get_users
from repository.users import create_user
from mapper.buttonMapper import get_handler
from external.deepinfra import createRequest

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
    markup.add(telebot.types.KeyboardButton(config['Buttons']['takeTime']))
    markup.add(telebot.types.KeyboardButton(config['Buttons']['getData']))
    bot.send_message(message.chat.id, "Теперь тебе доступен функционал бота", reply_markup=markup)

@bot.message_handler()
def handle_message(message):
    print(message.text, "sfdgh")
    handler = get_handler(message.text)
    if handler is not None:
        handler(message)
    else:
        bot.send_message(message.chat.id,"Выбери из предложенного, не пиши сам")
        default_buttons(message)

def takeTime(message):
    bot.send_message(message.chat.id, "Вы выбрали время")

def getData(message):
    bot.send_message(message.chat.id, "Вы получаете отчетность")


@bot.message_handler(commands=['ai'])
def handle_ai(message):
    mess = 'Привет. Это тест. Напиши "Валера"'
    data = createRequest(mess)
    bot.send_message(message.chat.id, f"Оракул ответил:{data}")

bot.polling(none_stop=True)
