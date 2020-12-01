from elasticsearch import Elasticsearch, helpers
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')

index = 'notice'


with open('notice.json', 'r') as f:
    notice  = json.load(f)


docs = []

for doc in notice:
    docs.append({"_index": index,  "_source": doc})

ppr.pprint(docs)

#helpers.bulk(es, docs)
for doc in notice:
    ppr.pprint(doc)
    es.index(index=index, body=doc)

#ppr.pprint(es.cat.indices())
