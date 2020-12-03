from elasticsearch import Elasticsearch
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')

with open('notice_mapping.json', 'r') as f:
    notice_mapping = json.load(f)


if es.indices.exists(index='notice'):
    print(es.indices.delete(index='notice'))
print(es.indices.create(index='notice', body=notice_mapping))


ppr.pprint(es.cat.indices())
