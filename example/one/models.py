from django.db import models
from wormhole import wormhole

import time

@wormhole.register
def sleep(request, seconds):
    print seconds
    time.sleep(seconds)
    return True
