"""
WSGI config for newsdemo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

import multiprocessing

from django.core.wsgi import get_wsgi_application

from newsdemo.apps.crawler.tasks import schedule_crawler

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsdemo.settings")
# os.environ['DJANGO_SETTINGS_MODULE'] = 'newsdemo.settings'
application = get_wsgi_application()

schedule_crawler.delay()