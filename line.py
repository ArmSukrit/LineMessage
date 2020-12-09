import requests
from random import choice

from utils import time_log, get_and_save_token
from stickers import kinda_sad_stickers, kinda_happy_stickers
from exceptions import *
from global_vars import token_file


def send_line_message(message, token=None, imageThumbnail=None, imageFullsize=None, notificationDisabled=False,
                      stickerId=None, stickerPackageId=None, imageFile=None,
                      randSadStickers=False, randHappyStickers=False):
    """ send Line message with/without sticker, image
        For token, see more at https://notify-bot.line.me/my/
        For what can be sent see https://notify-bot.line.me/doc/en/
            topic: "POST https://notify-api.line.me/api/notify" -> "Request parameters"

        :return True if sent successfully else False """

    if not message:
        raise MessageNotGivenError("Message is required.")

    if not token:
        try:
            with open(token_file) as f:
                token = f.read().strip()
        except FileNotFoundError:
            try:
                with open("Line\\" + token_file) as f:
                    token = f.read().strip()
            except FileNotFoundError:
                token = get_and_save_token()

    if (randHappyStickers or randSadStickers) and (stickerId or stickerPackageId):
        raise StickerError("random sticker mode is on but stickerId or stickerPackageId is/are True")

    if randHappyStickers and randSadStickers:
        raise ConflictRandomSticker("Both randHappyStickers and randSadStickers are True. Only one can be chosen")
    if randSadStickers or randSadStickers:
        if randSadStickers:
            sticker = choice(kinda_sad_stickers)
        else:
            sticker = choice(kinda_happy_stickers)
        stickerPackageId = sticker['stickerPackageId']
        stickerId = choice(sticker['stickerIds'])

    # only message is required, others are optional
    data = {
        'message': message,
        'imageThumbnail': imageThumbnail,
        'imageFile': imageFile,  # open("image.jpg", "rb")
        'stickerPackageId': stickerPackageId,  # stickers https://devdocs.line.me/files/sticker_list.pdf
        'stickerId': stickerId,  # stickers https://devdocs.line.me/files/sticker_list.pdf
        'notificationDisabled': notificationDisabled,
        'imageFullsize': imageFullsize,
    }

    url = 'https://notify-api.line.me/api/notify'
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
    r = requests.post(url, headers=headers, data=data)
    if r.status_code == 200:
        time_log("Sent message to Line.")
        return True
    else:
        time_log(f"Cannot send Line message, '{eval(r.text)['message']}'")
        return False


if __name__ == '__main__':
    """ run this to input your token """
    get_and_save_token()
