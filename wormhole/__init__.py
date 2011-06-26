from WormholeCall import WormholeCall
from django.conf import settings
from django.utils.importlib import import_module

wormhole = WormholeCall()

def wormhole_autodiscover():
    for app in settings.INSTALLED_APPS:
        try:
            import_module('%s.ajax'% app)
        except:
            # no app.wormhole, so just fail silently
            pass

wormhole_autodiscover()
