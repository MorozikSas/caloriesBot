import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def get_handler(text):
    buttons = config['Buttons']
    handler_name = buttons.get(text)
    print(handler_name)
    if text == handler_name:
        print(handler_name)
        return globals().get(handler_name, None)
    # for key, value in buttons.items():
        # if text == value:
        #     handler_function_name = buttons.get(key)
        #     if handler_function_name:
        #         return globals().get(handler_function_name, None)
    return None
