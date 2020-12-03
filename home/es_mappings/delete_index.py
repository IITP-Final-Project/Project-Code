import sys

from elasticsearch import Elasticsearch

import json
import pprint as ppr




es = Elasticsearch('localhost:9200')

index = sys.argv[1]


ppr.pprint(es.indices.delete(index=index))
