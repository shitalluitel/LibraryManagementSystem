"""
WSGI config for LibraryManagementSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from my_project import MyWSGIApp

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryManagementSystem.settings")

application = MyWSGIApp()
application = WhiteNoise(application, root='staticfiles')
# application.add_files()
