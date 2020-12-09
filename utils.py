from datetime import datetime


def time_log(message='', end='\n'):
    """ usage:
            print(f"{time_log()}: some messages")  # do not provide any argument
            or time_log("some messages")  # use like normal print() """

    if message:
        print(f"{datetime.now().strftime('%H:%M:%S.%f')}: {message}", end=end)
    else:
        return datetime.now().strftime('%H:%M:%S.%f')
