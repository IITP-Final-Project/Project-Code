from elasticsearch import Elasticsearch, helpers
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')

index = 'lecture_rate'


with open('lecture_rate.json', 'r') as f:
    lecture_rate = json.load(f)


docs = []

for doc in lecture_rate:
    docs.append({"_index": index,  "_source": doc})

ppr.pprint(docs)

#helpers.bulk(es, docs)
for doc in lecture_rate:
    ppr.pprint(doc)
    es.index(index=index, body=doc)

#ppr.pprint(es.cat.indices())
