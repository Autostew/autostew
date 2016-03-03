name = 'DB'


def init(server):
    import os, sys

    #proj_path = "/path/to/my/project/"
    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autostew.settings")
    #sys.path.append(proj_path)

    # This is so my local_settings.py gets loaded.
    #os.chdir(proj_path)

    # This is so models get loaded.
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

init(None)

def tick(server):
    pass

def event(server, event):
    pass