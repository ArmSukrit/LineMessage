class Error(Exception):
    pass


class StickerError(Error):
    """ base error about stickers """
    pass


class ConflictRandomSticker(StickerError):
    """ raise when True is given to both randomSticker params """
    pass
