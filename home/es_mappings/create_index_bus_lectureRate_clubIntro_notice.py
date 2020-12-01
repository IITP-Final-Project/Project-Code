from elasticsearch import Elasticsearch
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')

with open('bus_mapping.json', 'r') as f:
    bus_mapping = json.load(f)

with open('lecture_rate_mapping.json', 'r') as f:
    lecture_rate_mapping = json.load(f)

with open('club_intro_mapping.json', 'r') as f:
    club_intro_mapping = json.load(f)

with open('notice_mapping.json', 'r') as f:
    notice_mapping = json.load(f)


if es.indices.exists(index='bus'):
    print(es.indices.delete(index='bus'))
print(es.indices.create(index='bus', body=bus_mapping))

if es.indices.exists(index='lecture_rate'):
    print(es.indices.delete(index='lecture_rate'))
print(es.indices.create(index='lecture_rate', body=lecture_rate_mapping))

if es.indices.exists(index='club_intro'):
    print(es.indices.delete(index='club_intro'))
print(es.indices.create(index='club_intro', body=club_intro_mapping))

if es.indices.exists(index='notice'):
    print(es.indices.delete(index='notice'))
print(es.indices.create(index='notice', body=notice_mapping))


ppr.pprint(es.cat.indices())
