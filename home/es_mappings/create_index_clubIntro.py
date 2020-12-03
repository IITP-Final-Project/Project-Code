from elasticsearch import Elasticsearch
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')

with open('club_intro_mapping.json', 'r') as f:
    club_intro_mapping = json.load(f)


if es.indices.exists(index='club_intro'):
    print(es.indices.delete(index='club_intro'))
print(es.indices.create(index='club_intro', body=club_intro_mapping))


ppr.pprint(es.cat.indices())
