import requests
import os
import django
import datetime
import json
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot.settings")
django.setup()

from plan.models import Plan

temp = Plan.objects.all()
temp.delete()
