import sys

from elasticsearch import Elasticsearch

import json
import pprint as ppr



index = sys.argv[1]

es = Elasticsearch('localhost:9200')



res = es.search(index=index, body={"query": {"match_all": {}}})

ppr.pprint(res)
