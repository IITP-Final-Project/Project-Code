from elasticsearch import Elasticsearch
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')

with open('schedule_mapping.json', 'r') as f:
    schedule_mapping = json.load(f)


if es.indices.exists(index='schedule'):
    print(es.indices.delete(index='schedule'))
print(es.indices.create(index='schedule', body=schedule_mapping))


ppr.pprint(es.cat.indices())
