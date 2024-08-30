import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def get_handler(text):
    buttons = config['Buttons']
    for key, value in buttons.items():
        if text == value:
            return key
    return None
