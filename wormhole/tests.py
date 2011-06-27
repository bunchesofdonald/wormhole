from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import simplejson

from wormhole import wormhole, status

@wormhole.register
def to_upper(request, word):
    return word.upper()

class CallbackTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_callback(self):
        # Call to_upper
        word = 'testing'
        resp = self.client.post(reverse('wormhole_call'),
                {'name': 'to_upper', 'args': '{"word":"%s"}' % word })

        return_object = simplejson.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(return_object['status'], status.WORMHOLE_OK)
        self.assertEqual(return_object['errors'], [])
        self.assertEqual(return_object['result'], word.upper())

        # Send a non-existent function name
        resp = self.client.post(reverse('wormhole_call'),
                {'name': 'wormhole_this_does_not_extist', 'args': '{}'})

        return_object = simplejson.loads(resp.content)
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(return_object['status'], status.WORMHOLE_ERROR)
        self.assertEqual(return_object['errors'], [status.WORMHOLE_FUNCTION_NOT_FOUND])
        self.assertEqual(return_object['result'], None)

        # Send no function name
        resp = self.client.post(reverse('wormhole_call'), {'args': '{}'})

        return_object = simplejson.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(return_object['status'], status.WORMHOLE_ERROR)
        self.assertEqual(return_object['errors'], [status.WORMHOLE_FUNCTION_NAME_NOT_FOUND])
        self.assertEqual(return_object['result'], None)
        
        # Send no function name or args
        resp = self.client.post(reverse('wormhole_call'), {})

        return_object = simplejson.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(return_object['status'], status.WORMHOLE_ERROR)
        self.assertEqual(return_object['errors'], [status.WORMHOLE_FUNCTION_NAME_NOT_FOUND])
        self.assertEqual(return_object['result'], None)
        
    def test_resolve(self):
        wormhole_resolve_url = reverse('wormhole_resolve')
        resp = self.client.post(wormhole_resolve_url, 
                {'name': 'wormhole_resolve','args':''})

        return_object = simplejson.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(return_object['status'], status.WORMHOLE_OK)
        self.assertEqual(return_object['errors'], [])
        self.assertEqual(return_object['result'], wormhole_resolve_url)
        
        # Send non-existent view_name
        resp = self.client.post(wormhole_resolve_url, 
                {'name': 'wormhole_this_does_not_exist','args':''})

        return_object = simplejson.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(return_object['status'], status.WORMHOLE_ERROR)
        self.assertEqual(return_object['errors'], [status.WORMHOLE_NO_REVERSE_MATCH])
        self.assertEqual(return_object['result'], None)
