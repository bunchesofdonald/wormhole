import logging

from wormhole import status

from django.utils import simplejson
from django.http import HttpResponse
from django.core.urlresolvers import reverse, NoReverseMatch


class WormholeCall(object):
    '''
    methods:
        get_return_object - Creates a boilerplate return_object.
        register - A decorator. Adds the function to Wormholes callbacks.
        call - Gets a request, looks up the function to call in the
            callbacks. Returns an HttpResponse containing the result of
            the function

        resolve - A proxy to django.reverse.
    '''

    def __init__(self):
        '''init a WormholeCall object'''
        self.callbacks = {}
        self.logger = logging.getLogger('wormhole')

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
        #       also add support for wormhole.register(name='my_name')

        self.callbacks[func.__name__] = func

    def get_return_object(self):
        ''' Get a boilerplate return_object '''
        return {'status': None, 'errors': [], 'result': None}

    def get_call_name(self, request):
        return request.POST.get('name')

    def get_call_args(self, request):
        kwargs = {}
        json_args = request.POST.get('args')

        if json_args:
            json_args = simplejson.loads(json_args)
            for arg in json_args:
                kwargs[arg.encode('ascii', 'replace')] = json_args[arg]

        return kwargs

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

        return_object = self.get_return_object()
        function_name = self.get_call_name(request)
        function_kwargs = self.get_call_args(request)

        if function_name == None:
            return_object['status'] = status.WORMHOLE_ERROR
            return_object['errors'].append(status.WORMHOLE_FUNCTION_NAME_NOT_FOUND)
            self.logger.error(status.WORMHOLE_FUNCTION_NAME_NOT_FOUND)

        else:
            try:
                return_object['status'] = status.WORMHOLE_OK
                return_object['result'] = self.callbacks[function_name](request, **function_kwargs)
            except KeyError:
                return_object['status'] = status.WORMHOLE_ERROR
                return_object['errors'].append(status.WORMHOLE_FUNCTION_NOT_FOUND)
                self.logger.error(status.WORMHOLE_FUNCTION_NOT_FOUND)

        return self.response(return_object)

    def resolve(self, request):
        '''
        A proxy to django.reverse

        POST Params:
            name : Function name or URL Pattern name of view
            args : kwargs to pass to reverse

        Returns an HttpResponse with a json object:
            {"status": "ok", "errors": [], "result": "/index/"}
        '''
        view_name = self.get_call_name(request)
        reverse_kwargs = self.get_call_args(request)
        return_object = self.get_return_object()

        try:
            return_object['status'] = status.WORMHOLE_OK
            return_object['result'] = reverse(view_name, **reverse_kwargs)
        except NoReverseMatch:
            return_object['status'] = status.WORMHOLE_ERROR
            return_object['errors'].append(status.WORMHOLE_NO_REVERSE_MATCH)
            self.logger.error(status.WORMHOLE_NO_REVERSE_MATCH)
        
        return self.response(return_object)

    def response(self, return_object):
        ''' Encodes the return_object into json and returns it in an HttpResponse '''
        return HttpResponse(simplejson.dumps(return_object),
                mimetype="application/json")
