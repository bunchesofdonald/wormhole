import time
from wormhole import wormhole

@wormhole.register
def sleep(request, seconds):
    time.sleep(seconds)
    return True
