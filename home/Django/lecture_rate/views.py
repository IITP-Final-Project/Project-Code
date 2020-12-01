from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count
from elasticsearch import Elasticsearch

# Create your views here.

@csrf_exempt
def start_lecture(request): 
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    search = return_act['search']['origin']
    es = Elasticsearch('localhost:9200')
    index = 'lecture_rate'
    search_field = 'context'
    body = {
            'query':{
                'bool':{
                    'should':[
                        {'term':{'lecture':search}},
                        {'term':{'teacher':search}},
                        {'term':{'context':search}}
                        ],
                    }
                }
            }
    res = es.search(index=index, body=body)

    result1 = []
    result2 = []
    result3 = []
    if len(res['hits']['hits']) != 0:
        for hit in res['hits']['hits']:
            result1.append(hit['_source']['lecture'])
            result2.append(hit['_source']['teacher'])
            result3.append(hit['_source']['context'])
            msg = '\''+search+'\' 검색 결과입니다.\n\n'
            for i in range(len(result1)):
                msg += str(i+1)+'.\n강의명: '+result1[i]+'\n교수명: '+result2[i]+'\n평가: '+result3[i]+'\n\n'
    else:
        msg = '검색 결과가 없습니다.'

    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': msg
                    }
                }],
            'quickReplies': [{
                'label': '처음으로',
                'action': 'message',
                'messageText': '처음으로'
                }]
            }
        })

@csrf_exempt
def test(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']


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



