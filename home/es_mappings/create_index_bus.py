from elasticsearch import Elasticsearch
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')

with open('bus_mapping.json', 'r') as f:
    bus_mapping = json.load(f)


if es.indices.exists(index='bus'):
    print(es.indices.delete(index='bus'))
print(es.indices.create(index='bus', body=bus_mapping))


ppr.pprint(es.cat.indices())
