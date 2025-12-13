import os

from django.core.wsgi import get_wsgi_application

# Point to your settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RetailPulse.settings')

# This is the 'application' the error says is missing
application = get_wsgi_application()