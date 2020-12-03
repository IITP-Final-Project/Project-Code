from elasticsearch import Elasticsearch
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')

with open('test_lecture_rate_mapping.json', 'r') as f:
    test_lecture_rate_mapping = json.load(f)


if es.indices.exists(index='test'):
    print(es.indices.delete(index='test'))
print(es.indices.create(index='test', body=test_lecture_rate_mapping))


ppr.pprint(es.cat.indices())
