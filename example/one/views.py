from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request, template_name='one/index.html'):
    return render_to_response(template_name, RequestContext(request, {}))
