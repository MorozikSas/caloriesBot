from service.config import Buttons

def get_handler(text):
    for key in Buttons.__dict__:
        if Buttons.__dict__[key] == text:
            return key
    return None