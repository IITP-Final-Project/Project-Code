from elasticsearch import Elasticsearch
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')


with open('lecture_rate_mapping.json', 'r') as f:
    lecture_rate_mapping = json.load(f)


if es.indices.exists(index='lecture_rate'):
    print(es.indices.delete(index='lecture_rate'))
print(es.indices.create(index='lecture_rate', body=lecture_rate_mapping))


ppr.pprint(es.cat.indices())
