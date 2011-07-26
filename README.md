# Wormhole

A Django/jQuery app that makes it dead simple to make calls to python through javascript.

## Installation

    git clone git://github.com/bunchesofdonald/wormhole.git
    ln -s wormhole/wormhole /path/to/my/project/wormhole
    
Add 'wormhole' to your settings.INSTALLED_APPS

## Quick Start

    python manage startapp myapp

Edit myapp/ajax.py to:

    from wormhole import wormhole

    @wormhole.register
    def say_my_name(request, name):
        return 'Hello %s' % name

In your view html, include the wormhole.js:
    `<script src="{{ STATIC_URL }}wormhole.js?csrf_token={{ csrf_token }}"></script>`

Notice that is {{ csrf_token }} (double brackets) NOT {% csrf_token %}. 
The latter creates an input element, the former is the value.

and then make a call to our say_my_name function:

    $.wormhole.rpc('say_my_name', {'name':'Chris'}, function(data) { alert(data.result); })
