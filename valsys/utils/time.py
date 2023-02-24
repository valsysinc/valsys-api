import datetime


def time(d=0):
    return (datetime.datetime.utcnow() -
            datetime.timedelta(days=d)).isoformat() + "Z"


def yesterday():
    return time(1)


def today():
    return time()


def tomorrow():
    return time(-1)
