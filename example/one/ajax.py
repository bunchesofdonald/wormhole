import time
from wormhole import wormhole

@wormhole.register
def sleep(request, seconds):
    print seconds
    time.sleep(seconds)
    return True
