from elasticsearch import Elasticsearch


es = Elasticsearch('localhost:9200')

print(es.cat.indices())
