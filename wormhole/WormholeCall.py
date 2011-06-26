from django.utils import simplejson
from django.http import HttpResponse

class WormholeCall(object):
    def __init__(self):
        '''
        init a WormholeCall object
        '''
        self.callbacks = {}

    def register(self, func):
        self.callbacks[func.__name__] = func

    def call(self, request):
        function_name = request.POST.get('name')
        json_args = simplejson.loads(request.POST.get('kwargs'))['args']

        function_kwargs = {}
        for arg in json_args:
            function_kwargs[str(arg)] = json_args[arg]

        result = self.callbacks[function_name](request, **function_kwargs)
        
        return HttpResponse(simplejson.dumps(result), mimetype="application/json") 
