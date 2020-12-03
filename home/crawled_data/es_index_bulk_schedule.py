import sys
from elasticsearch import Elasticsearch
import datetime
import pprint as ppr


es = Elasticsearch('localhost:9200')

userID = sys.argv[1]
now = datetime.datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')


schedules = []

for i in range(6):
    deadline = now
    subject = '테스트 일정 ' + str(i + 1)
    place = '테스트 장소 ' + str(i + 1)
    schedules.append({'userID': userID, 'deadline': deadline, 'subject': subject, 'place': place})
    ppr.pprint({'userID': userID, 'deadline': deadline, 'subject': subject, 'place': place})

for i in range(4):
    deadline = tomorrow
    subject = '테스트 내일 일정 ' + str(i + 1)
    place = '테스트 내일 장소 ' + str(i + 1)
    schedules.append({'userID': userID, 'deadline': deadline, 'subject': subject, 'place': place})
    ppr.pprint({'userID': userID, 'deadline': deadline, 'subject': subject, 'place': place})


for schedule in schedules:
    ppr.pprint(es.index(index='schedule', body=schedule))


es.indices.refresh(index='schedule')
