import logging as lg

from wormhole import errors

from django.utils import simplejson
from django.http import HttpResponse
from django.core.urlresolvers import reverse

class WormholeCall(object):
    def __init__(self):
        '''
        init a WormholeCall object

        methods:
            register - A decorator. Adds the function to Wormholes callbacks.
            call - Gets a request, looks up the function to call in the
                callbacks. Returns an HttpResponse containing the result of 
                the function
            
            resolve - A proxy to django.reverse. 
        '''
        self.callbacks = {}

    def register(self, func):
        '''
        Registers the given function with Wormhole callbacks.

        Used as a decorator:
            @wormhole.register
            def sleep(seconds):
                time.sleep(seconds)
                return True
        '''
        #TODO - Make this more than just a decorator, so that
        #       wormhole.register(some_function) is supported.

        self.callbacks[func.__name__] = func

    def call(self, request):
        '''
        Calls the given function and returns an HttpResponse with a json 
        object containing two attrubutes:
            result : The return result of the function
            status : 'ok' or 'error'
            errors : Error detail
            
            {"status": "ok", "result": "true", "errors": [] }
            {"status": "error", "result": "true", "errors": [... list of errors... ]  }

        Expects two parameters via POST:
            name : The name of the function to call
            args : A Json object of the kwargs to relay to the function
        '''

        wormhole_json = {
            'status' : 'ok',
            'errors' : [],
            'result' : None
        }

        if "name" not in request.POST:
            wormhole_json['status'] = errors.WORMHOLE_ERROR
            wormhole_json['error'].append(errors.WORMHOLE_FUNCTION_NAME_NOT_FOUND)
        
        function_name = request.POST.get('name')
        json_args = simplejson.loads(request.POST.get('args'))

        function_kwargs = {}
        for arg in json_args:
            try:
                function_kwargs[str(arg)] = json_args[arg]
            except:
                wormhole_json['status'] = errors.WORMHOLE_ERROR
                wormhole_json['error'].append(errors.WORMHOLE_FUNCTION_NAME_NOT_VALID)

        result = self.callbacks[function_name](request, **function_kwargs)

        if result:
            wormhole_json['result'] = result
        else:
            wormhole_json['status'] = errors.WORMHOLE_ERROR
            wormhole_json['error'].append(errors.WORMHOLE_NO_RESULT)
        
        return HttpResponse(simplejson.dumps(wormhole_json), mimetype="application/json") 

    def resolve(self, request):
        '''
        A proxy to django.reverse

        POST Params:
            name : Function name or URL Pattern name of view
            [args] : Optional kwargs to pass to reverse

        Returns an HttpResponse with a json object:
            {"status": "ok", "result": "/index/" }
        '''
        view_name = request.POST.get('name')
        try:
            json_args = simplejson.loads(request.POST.get('args', ""))
        except ValueError:
            json_args = None

        view_url = reverse(view_name, kwargs=json_args)
        
        return HttpResponse(simplejson.dumps({'status': 'ok', 'result': view_url}))
