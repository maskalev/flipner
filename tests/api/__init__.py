import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "flipner.settings")

django.setup()
