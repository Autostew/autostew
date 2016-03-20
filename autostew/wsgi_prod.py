import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/autostew')
os.environ["DJANGO_SETTINGS_MODULE"] = "autostew.settings.prod"

application = get_wsgi_application()
