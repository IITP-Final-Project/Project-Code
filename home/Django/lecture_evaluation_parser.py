import requests
import os
import django
import datetime
import json
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot.settings")
django.setup()

from parsed_data.models import lecture_rate

temp = lecture_rate.objects.filter(rate=1)
for i in range(len(temp)):
    print(i)
    print(temp[i])
    print('\n')
temp15= temp[15]
print(temp15.lecture)

#with open('lecture_rate.json','r') as lecturerate:
#    json_list = json.load(lecturerate)
#    json_list.reverse()
#    for i in json_list:
#        lecture_rate.objects.create(lecture = i['lecture'],teacher=i['teacher'],rate=i['rate'],semester = i['semester'],context=i['context'])
