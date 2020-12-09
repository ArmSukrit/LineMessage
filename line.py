import requests

from utils import time_log, get_and_save_token, random_sticker
from stickers import kinda_sad_stickers, kinda_happy_stickers
from exceptions import *
from global_vars import token_file


def send_line_message(message, token=None,
                      imageFile=None, imageThumbnail=None, imageFullsize=None,
                      stickerId=None, stickerPackageId=None,
                      randSadStickers=False, randHappyStickers=False,
                      notificationDisabled=False,
                      report=True):
    """ send Line message with/without sticker, image
        For token, see more at https://notify-bot.line.me/my/
        For what can be sent see https://notify-bot.line.me/doc/en/
            topic: "POST https://notify-api.line.me/api/notify" -> "Request parameters"

        param report: print to console when finished if True else no printing
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

    # random sticker
    if randHappyStickers and randSadStickers:
        raise ConflictRandomSticker("Both randHappyStickers and randSadStickers are True. Only one can be chosen")
    if randSadStickers or randSadStickers:
        if randSadStickers:
            stickerPackageId, stickerId = random_sticker(kinda_sad_stickers)
        else:
            stickerPackageId, stickerId = random_sticker(kinda_happy_stickers)

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
        if report:
            time_log("Sent message to Line.")
        return True
    else:
        if report:
            time_log(f"Cannot send Line message, '{eval(r.text)['message']}'")
        return False


if __name__ == '__main__':
    """ run this to input your token """
    get_and_save_token()
