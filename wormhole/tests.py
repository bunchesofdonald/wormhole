"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

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

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, '{"status": "ok", "errors": [], "result": "TESTING"}')

    def test_resolve(self):
        wormhole_resolve_url = reverse('wormhole_resolve')
        resp = self.client.post(wormhole_resolve_url, 
                {'name': 'wormhole_resolve','args':''})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, '{"status": "ok", "errors": [], "result": "/wormhole/resolve"}')
