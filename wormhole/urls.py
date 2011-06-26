from django.conf.urls.defaults import patterns, include, url

from wormhole import wormhole

urlpatterns = patterns('',
    url(r'wormhole/call', wormhole.call, name='wormhole_call'),
)
