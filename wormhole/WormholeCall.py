from wormhole import errors

from django.utils import simplejson
from django.http import HttpResponse
from django.core.urlresolvers import reverse

class WormholeCall(object):
    def __init__(self):
        '''
        init a WormholeCall object
        '''
        self.callbacks = {}

    def register(self, func):
        self.callbacks[func.__name__] = func

    def call(self, request):
        print 'this is a test'
        wormhole_json = {}

        #if "name" not in request.POST:
         #   wormhole_json['status'] = errors.WORMHOLE_ERROR
          #  wormhole_json['error'] = errors.WORMHOLE_FUNCTION_NAME_NOT_FOUND

        function_name = request.GET.get('name')
        json_args = simplejson.loads(request.GET.get('kwargs'))

        function_kwargs = {}
        for arg in json_args:
            # TODO: try/except on the translation to string.
            function_kwargs[str(arg)] = json_args[arg]

        result = self.callbacks[function_name](request, **function_kwargs)

        if result:
            wormhole_json['status'] = 'ok'
            wormhole_json['result'] = result
        
        return HttpResponse(simplejson.dumps(wormhole_json), mimetype="application/json") 

    def resolve(request):
        # reverse(viewname[, urlconf=None, args=None, kwargs=None, current_app=None])

        pass
