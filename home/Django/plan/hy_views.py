#from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
#from plan.models import Plan2
import datetime
from datetime import timedelta
#from django.db.models import Count
#import re
from elasticsearch import Elasticsearch

from .DecodeAnswer import *

# Create your views here.

# Schedule Welcome Function
@csrf_exempt
def Schedule(request):
	userID, context = DecodeAnswer(request)
	
	## Searching Query Setting
	es = Elasticsearch('localhost:9200')
	index = 'schedule'
	body = {
		"query": {
			"bool": {
				"must": [{
					"term": {
						"deadline": {
							"value": datetime.datetime.now().strftime('%Y-%m-%d')
						}
					}
				}],
				"filter": [{
					"term": {
						"userID": userID
					}
				}],
			}
		}
	}

	## Searching. . .
	res = es.search(index=index, body=body)

	count = res['hits']['total']['value']
	schedules = res['hits']['hits']

	## Response Building
	response = str(userID) + '!\n오늘 니 일정이 ' + str(count) + '개 있단다.\n'
	
	## Today Schedule List-up
	if count > 5:
		for schedule in schedules[:5]:
			response += '\nsubject: ' + str(schedule['_source']['subject'])
			response += '\nplace: ' + str(schedule['_source']['place'])
			response += '\n\n'
		response += '오늘 이 외에도 ' + str(count - 5) + '개의 일정이 있으니까'
		response += '\n전체 조회를 해보든가 말든가\n\n'
	else:
		for schedule in schedules:
			response += '\nsubject: ' + str(schedule['_source']['subject'])
			response += '\nplace: ' + str(schedule['_source']['place'])
			response += '\n\n'

	response += '어쩔래?\n'

	## Response finish
	response_end = '------ 응답 끝 ------\n'
	response += response_end
	return JsonResponse({
		"version": "2.0",
		"template": {
			"outputs": [{
				"basicCard": {
					"description": response,
					"buttons": [
						{
							"label": "전체 일정 보여주세요 ㅠㅠ",
							"action": "message",
							"messageText": "호열 전체 일정 조회"
						},
						{
							"label": "처음으로 돌아가라",
							"action": "message",
							"messageText": "호열 테스트"
						}
					]
				}
			}],
			"quickReplies": [
				{
					"label": "호열 테스트",
					"action": "message",
					"messageText": "호열 테스트"
				},
				{
					"label": "처음으로",
					"action": "message",
					"messageText": "처음으로"
				}
			]
		}
	})
	

# Checking entire schedule function
@csrf_exempt
def EntireSchedule(request):
	userID, context = DecodeAnswer(request)

	## Searching Query Setting
	es = Elasticsearch('localhost:9200')
	index = 'schedule'
	body = {
		"aggs": {
			"daily_count": {
				"terms": {
					"field": "deadline"
				}
			}
		},
		
		"query": {
			"term": {
				"userID": userID
			}
		}
	}

	## Searching. . .
	res = es.search(index=index, body=body)

	count = res['hits']['total']['value']
	schedules = res['hits']['hits']

	## Responses Building
	response = str(userID) + '님의 전체 일정 조회 결과입니다.'
	response += '\n총 ' + str(count) + '개의 일정이 있습니다.'

	## Entire schedule list-up
	#for schedule in schedules['hits']['hits'][:5]:


	
	## Response finish
	response_end = '\n------ 응답 끝 ------\n'
	response += response_end
	return JsonResponse({
		"version": "2.0",
		"template": {
			"outputs": [{
				"basicCard": {
					"description": response,
					"buttons": [
						{
							"label": "전체 일정 보여주세요 ㅠㅠ",
							"action": "message",
							"messageText": "호열 전체 일정 조회"
						},
						{
							"label": "처음으로 돌아가라",
							"action": "message",
							"messageText": "호열 테스트"
						}
					]
				}
			}],
			"quickReplies": [
				{
					"label": "호열 테스트",
					"action": "message",
					"messageText": "호열 테스트"
				},
				{
					"label": "처음으로",
					"action": "message",
					"messageText": "처음으로"
				}
			]
		}
	})
















@csrf_exempt
def planning(request):
    raw_answer = request.body.decode('utf-8')
    answer = json.loads(raw_answer)

    userID = answer['userRequest']['user']['properties']['plusfriendUserKey']
    context = answer['userRequest']['utterance']

    response = '유저 아이디(userID)는 ' + str(userID) + ' 입니다.\n' + '그리고 사용자가 입력한 내용은 ' + str(context) + ' 입니다.\n\n끝!' 
    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'basicCard': {
                    'description': response,
                    'buttons': [
                        {
                            'label': '돌아가자!',
                            'action': 'message',
                            'messageText': '처음으로'
                        }
                    ],
                }}],
            'quickReplies': [
                {
                    'label': '처음으로',
                    'action': 'message',
                    'messageText': '처음으로'
                }]
        }
    })




