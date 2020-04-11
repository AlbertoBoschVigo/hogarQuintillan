"""
ASGI config for hogarQuintillan project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
import django
from channels.routing import get_default_application

#from django.conf import settings

#settings.configure()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hogarQuintillan.settings")
django.setup()
application = get_default_application()