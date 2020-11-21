"""
WSGI config for bot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/home/Django')
sys.path.append('/home/Django/myvenv/lib/python3.6/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot.settings')

application = get_wsgi_application()
