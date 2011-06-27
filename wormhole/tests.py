from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.utils import simplejson

from wormhole import wormhole

@wormhole.register
def to_upper(request, word):
    return word.upper()

class CallbackTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_callback(self):
        word = 'testing'
        resp = self.client.post(reverse('wormhole_call'),
                {'name': 'to_upper', 'args': '{"word":"%s"}' % word })

        return_object = simplejson.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(return_object['status'], 'ok')
        self.assertEqual(return_object['errors'], [])
        self.assertEqual(return_object['result'], word.upper())

    def test_resolve(self):
        wormhole_resolve_url = reverse('wormhole_resolve')
        resp = self.client.post(wormhole_resolve_url, 
                {'name': 'wormhole_resolve','args':''})

        return_object = simplejson.loads(resp.content)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(return_object['status'], 'ok')
        self.assertEqual(return_object['errors'], [])
        self.assertEqual(return_object['result'], wormhole_resolve_url)
