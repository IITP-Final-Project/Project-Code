from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from datetime import timedelta
from django.db.models import Count
from elasticsearch import Elasticsearch
# Create your views here.
@csrf_exempt
def start_club(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    now = datetime.date.today()
    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': '동아리 시작'
                    }
                }]
            }
        })

@csrf_exempt
def test(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    now = datetime.date.today()

    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': '테스트 성공'
                        }
                }]
            }
        })



