from elasticsearch import Elasticsearch, helpers
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')

index = 'club_intro'


with open('club_intro.json', 'r') as f:
    club_intro  = json.load(f)


docs = []

for doc in club_intro:
    docs.append({"_index": index,  "_source": doc})

ppr.pprint(docs)

#helpers.bulk(es, docs)
for doc in club_intro:
    ppr.pprint(doc)
    es.index(index=index, body=doc)

#ppr.pprint(es.cat.indices())
