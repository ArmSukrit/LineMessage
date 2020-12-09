from datetime import datetime
from random import choice

from global_vars import token_file


def time_log(message='', end='\n'):
    """ usage:
            print(f"{time_log()}: some messages")  # do not provide any argument
            or time_log("some messages")  # use like normal print() """

    if message:
        print(f"{datetime.now().strftime('%H:%M:%S.%f')}: {message}", end=end)
    else:
        return datetime.now().strftime('%H:%M:%S.%f')


def get_and_save_token():
    token = input("Line Notify token: ").strip()
    with open(token_file, 'w') as f:
        f.write(token)
    return token


def random_sticker(stickers: list):
    sticker = choice(stickers)
    return sticker['stickerPackageId'], choice(sticker['stickerIds'])
