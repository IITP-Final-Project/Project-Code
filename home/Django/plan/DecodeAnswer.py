from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from elasticsearch import Elasticsearch

import datetime




############################################################

def DecodeAnswer(request):
	
	raw_answer = request.body.decode('utf-8')
	answer = json.loads(raw_answer)

	userID = answer['userRequest']['user']['properties']['plusfriendUserKey']
	context = answer['userRequest']['utterance']

	return answer, userID, context