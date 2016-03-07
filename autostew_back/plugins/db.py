name = 'DB'


def init(server):
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autostew.settings")
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()
