import time
from wormhole import wormhole


@wormhole.register
def sleep(request, seconds):
    time.sleep(seconds)
    return True


@wormhole.register
def get_name(request, name):
    return "<b>Hello %s!</b>" % name
