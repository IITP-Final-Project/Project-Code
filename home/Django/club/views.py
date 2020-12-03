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
                'carousel': {
                    'type': 'basicCard',
                    'items': [
                        {
                            'description': '\'검색\'을 입력하여 동아리를 직접 검색하거나 버튼을 통해 목록을 선택할 수 있어요.',
                            'buttons': [
                                {
                                    'label': '과학기술분과',
                                    'action': 'message',
                                    'messageText': '과학기술분과'
                                    },
                                {
                                    'label': '봉사분과',
                                    'action': 'message',
                                    'messageText': '봉사분과'
                                    },
                                {
                                    'label': '연행예술분과',
                                    'action': 'message',
                                    'messageText': '연행예술분과'
                                    }
                                ]
                        },
                        {
                            'description': '\'검색\'을 입력하여 동아리를 >직접 검색하거나 버튼을 통해 목록을 선택할 수 있어요.',
                            'buttons': [
                                {
                                    'label': '전시창작분과',
                                    'action': 'message',
                                    'messageText': '전시창작분과'
                                    },
                                {
                                    'label': '종교분과',
                                    'action': 'message',
                                    'messageText': '종교분과'
                                    }
                                ]
                        },
                        {
                            'description': '\'검색\'을 입력하여 동아리를 직접 검색하거나 버튼을 통해 목록을 선택할 수 있어요.',
                            'buttons': [
                                {
                                    'label': '체육분과',
                                    'action': 'message',        
                                    'messageText': '체육분과'
                                    },
                                {
                                    'label': '학술분과',
                                    'action': 'message',
                                    'messageText': '학술분과'
                                    }
                                ]
                        }]
                    }}],
                'quickReplies': [
                    {
                        'label': '검색',
                        'action': 'message',
                        'messageText': '동아리 검색'
                    },
                    {
                        'label': '처음으로',
                        'action': 'message',
                        'messageText': '처음으로'
            }]
        }
    })

def show_club(category, name):
    es = Elasticsearch('localhost:9200')
    body = {
            'size':2,
            'query':{
                'bool':{
                    'should':[
                        {'term':{'category':category}}
                        ],
                    }
                }
            }
    res = es.search(index='club_intro', body=body)
    result1 = []
    result2 = []
    for hit in res['hits']['hits']:
        result1.append(hit['_source']['name'])
        result2.append(hit['_source']['explanation'])
        msg = name+'\n\n'
        for i in range(len(result1)):
            if len(result2[i]) > 120:
                msg += str(i+1)+'.\n동아리명: '+result1[i]+'\n소개: '+result2[i][0:120]+' (...) \n\n'
            else:
                msg += str(i+1)+'.\n동아리명: '+result1[i]+'\n소개: '+result2[i]+'\n\n'
    return msg

@csrf_exempt
def select_club(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    if return_str == '과학기술분과':
        msg= show_club('science_technology','과학기술분과')
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': msg,
                        'buttons' : [
                            {
                                'label': '자세히 보기',
                                'action': 'webLink',
                                'webLinkUrl': 'http://sejong.korea.ac.kr/campuslife/student/clubs/science_technology'
                                }]
                            }
                    }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action':'message',
                    'messageText': '처음으로'
                    }]
                }
            })
    elif return_str == '봉사분과':
        msg = show_club('volunteer_activities','봉사분과')
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': msg,
                        'buttons' : [
                            {
                                'label': '자세히 보기',
                                'action': 'webLink',
                                'webLinkUrl': 'http://sejong.korea.ac.kr/campuslife/student/clubs/volunteer_activities'
                                }]
                            }
                    }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action':'message',
                    'messageText': '처음으로'
                    }]
                }
            })
    elif return_str == '연행예술분과':
        msg = show_club('stage_arts','연행예술분과')
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': msg,
                        'buttons' : [
                            {
                                'label': '자세히 보기',
                                'action': 'webLink',
                                'webLinkUrl': 'http://sejong.korea.ac.kr/campuslife/student/clubs/stage_arts'
                                }]
                            }
                    }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action':'message',
                    'messageText': '처음으로'
                    }]
                }
            })
    elif return_str == '전시창작분과':
        msg = show_club('exhibition_creation','전시창작분과')
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': msg,
                        'buttons' : [
                            {
                                'label': '자세히 보기',
                                'action': 'webLink',
                                'webLinkUrl': 'http://sejong.korea.ac.kr/campuslife/student/clubs/exhibition_creation'
                                }]
                            }
                    }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action':'message',
                    'messageText': '처음으로'
                    }]
                }
            })

    elif return_str == '종교분과':
        msg = show_club('religion','종교분과')
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': msg,
                        'buttons' : [
                            {
                                'label': '자세히 보기',
                                'action': 'webLink',
                                'webLinkUrl': 'http://sejong.korea.ac.kr/campuslife/student/clubs/religion'
                                }]
                            }
                    }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action':'message',
                    'messageText': '처음으로'
                    }]
                }
            })
    elif return_str == '체육분과':
        msg = show_club('physical','체육분과')
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': msg,
                        'buttons' : [
                            {
                                'label': '자세히 보기',
                                'action': 'webLink',
                                'webLinkUrl': 'http://sejong.korea.ac.kr/campuslife/student/clubs/physical'
                                }]
                            }
                    }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action':'message',
                    'messageText': '처음으로'
                    }]
                }
            })
    elif return_str == '학술분과':
        msg = show_club('acadmic','학술분과')
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': msg,
                        'buttons' : [
                            {
                                'label': '자세히 보기',
                                'action': 'webLink',
                                'webLinkUrl': 'http://sejong.korea.ac.kr/campuslife/student/clubs/acadmic'
                                }]
                            }
                    }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action':'message',
                    'messageText': '처음으로'
                    }]
                }
            })

@csrf_exempt
def search_club(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    search = return_act['search']['origin']
    es = Elasticsearch('localhost:9200')
    body = {
        'query':{
            'bool':{
                'should':[
                    {'term':{'name':search}},
                    {'term':{'explanation':search}},
                    ],
                }
            }
        }
    res = es.search(index='club_intro', body=body)
    result1 = []
    result2 = []
    if len(res['hits']['hits']) != 0:
        for hit in res['hits']['hits']:
            result1.append(hit['_source']['name'])
            result2.append(hit['_source']['explanation'])
            msg = '\''+search+'\' 검색 결과입니다.\n\n'
            for i in range(len(result1)):
                msg += str(i+1)+'.\n동아리명: '+result1[i]+'\n소개: '+result2[i]+'\n\n'
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
