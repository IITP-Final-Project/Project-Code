from elasticsearch import Elasticsearch, helpers
import json
import pprint as ppr


es = Elasticsearch('localhost:9200')

index = 'bus'


with open('from_school.json', 'r') as f:
    from_school = json.load(f)

with open('from_school_sunday.json', 'r') as f:
    from_school_sunday = json.load(f)

with open('from_station.json', 'r') as f:
    from_station = json.load(f)

with open('from_station_sunday.json', 'r') as f:
    from_station_sunday = json.load(f)


for elem in from_school:
    elem["departure"] = "school"

for elem in from_school_sunday:
    elem["departure"] = "school"
    elem["sunday"] = True

for elem in from_station:
    elem["departure"] = "station"

for elem in from_station_sunday:
    elem["departure"] = "station"
    elem["sunday"] = True


times = []
for time in from_school:
    times.append(time)
for time in from_school_sunday:
    times.append(time)
for time in from_station:
    times.append(time)
for time in from_station_sunday:
    times.append(time)

#times.append(from_school)
#times.append(from_school_sunday)
#times.append(from_station)
#times.append(from_station_sunday)


docs = []

for doc in times:
    docs.append({"_index": index,  "_source": doc})

ppr.pprint(docs)

#helpers.bulk(es, docs)
for doc in times:
    ppr.pprint(doc)
    es.index(index=index, body=doc)

#ppr.pprint(es.cat.indices())
