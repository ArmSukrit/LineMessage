import requests

from utils import time_log


def send_line_message(message, token=None, imageThumbnail=None, imageFullsize=None, notificationDisabled=False,
                      stickerId=None, stickerPackageId=None, imageFile=None):
    """ send Line message with specific token.
        For token, see more at https://notify-bot.line.me/my/
        For what can be sent see https://notify-bot.line.me/doc/en/
            topic: "POST https://notify-api.line.me/api/notify" -> "Request parameters"

        :return True if sent successfully else False """

    if not message:
        time_log("message: must not be empty")
        return False

    if not token:
        token_file = "Line\\line_token.txt"
        try:
            with open(token_file) as f:
                token = f.read().strip()
        except FileNotFoundError:
            try:
                with open(token_file.replace("Line\\", '')) as f:
                    token = f.read().strip()
            except FileNotFoundError:
                print("You need to provide token of Line Notify.")
                return False

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
