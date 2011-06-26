from django.template import RequestContext
from django.shortcuts import render_to_response
from wormhole import wormhole

def index(request, template_name='one/index.html'):
    return render_to_response(template_name, RequestContext(request, {}))

@wormhole.register
def sleep(request, seconds):
	time.sleep(seconds)
	return True
