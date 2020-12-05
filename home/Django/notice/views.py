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
def start_notice(request):
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
                            'description': '\'검색\'을 입력하여 공지사항을 직접 검색하거나 버튼을 통해 목록을 선택할 수 있어요.',
                            'buttons': [
                                {
                                    'label': '코로나19(예방 및 대처)',
                                    'action': 'message',
                                    'messageText': '코로나19(예방 및 대처)'
                                    },
                                {
                                    'label': '코로나19(일정변경/조치)',
                                    'action': 'message',
                                    'messageText': '코로나19(일정변경 및 조치)'
                                    },
                                {
                                    'label': '학사일반',
                                    'action': 'message',
                                    'messageText': '학사일반'
                                    }
                                ]
                        },
                        {
                            'description': '\'검색\'을 입력하여 공지사항을 직접 검색하거나 버튼을 통해 목록을 선택할 수 있어요.',
                            'buttons': [
                                {
                                    'label': '교내행사',
                                    'action': 'message',
                                    'messageText': '교내행사'
                                    },
                                {
                                    'label': '장학',
                                    'action': 'message',
                                    'messageText': '장학'
                                    },
                                {
                                    'label': '진로취업',
                                    'action': 'message',
                                    'messageText': '진로취업'
                                    }
                                ]
                        }]
                    }}],
            'quickReplies': [
                {
                    'label': '검색',
                    'action': 'message',
                    'messageText': '공지 검색'
            }]
        }
    })

@csrf_exempt
def show_notice(category, name):
    es = Elasticsearch('localhost:9200')
    body = {
        'size':2,
        'sort':{
            'date':'desc'
            },
        'query':{
            'bool':{
                'should':[
                    {'term':{'category':category}}
                    ],
                }
            }
        }
    res = es.search(index='notice', body=body)
    result1 = []
    result2 = []
    result3 = []
    for hit in res['hits']['hits']:
        result1.append(hit['_source']['date'])
        result2.append(hit['_source']['title'])
        result3.append(hit['_source']['link'])
        msg = name+'\n\n'
        for i in range(len(result1)):
            msg += str(i+1)+'.\n작성일: '+result1[i]+'\n제목: '+result2[i]+'\n링크: '+result3[i]+'\n\n'
    return msg

@csrf_exempt
def select_notice(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    if return_str == '코로나19(예방 및 대처)':
        msg= show_notice('corona_prevent','코로나19(예방 및 대처)')
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
                                'webLinkUrl': 'http://sejong.korea.ac.kr/user/boardList.do?handle=102914&siteId=kr&id=kr_050108010000'
                                }]
                            }
                    }]
                }
            })
    elif return_str == '코로나19(일정변경 및 조치)' or return_str == '코로나' or return_str == '코로나19':
        msg = show_notice('corona_action','코로나19(일정변경 및 조치)')
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
                                'webLinkUrl': 'http://sejong.korea.ac.kr/user/boardList.do?handle=101685&siteId=kr&id=kr_050108020000'
                                }]
                            }
                    }]
                }
            })
    elif return_str == '학사일반' or return_str == '학사일반 공지' or return_str == '학사일반공지':
        msg = show_notice('common','학사일반공지')
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': msg,
                        'buttons' : [
                            {
                                'label': '자세히 보기',
                                'action': 'webLink',                                'webLinkUrl': 'http://sejong.korea.ac.kr/campuslife/notice/college'
                                }]
                            }
                    }]
                }
            })
    elif return_str == '교내행사' or return_str == '교내행사 공지' or return_str == '교내행사공지':
        msg = show_notice('event','교내행사공지')
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
                                'webLinkUrl': 'http://sejong.korea.ac.kr/user/boardList.do?handle=61751&siteId=kr&id=kr_050107000000'
                                }]
                            }
                    }]
                }
            })
    elif return_str == '장학' or return_str == '장학 공지' or return_str == '장학공지':
        msg = show_notice('scholarship','장학공지')
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
                                'webLinkUrl': 'http://sejong.korea.ac.kr/campuslife/notice/scholarship'
                                }]
                            }
                    }]
                }
            })
    elif return_str == '진로취업' or return_str == '진로취업 공지' or return_str == '진로취업공지':
        msg = show_notice('career','진로취업공지')
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
                                'webLinkUrl': 'http://sejong.korea.ac.kr/campuslife/notice/career'
                                }]
                            }
                    }]
                }
            })

@csrf_exempt
def search_notice(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    search = return_act['search']['origin']
    es = Elasticsearch('localhost:9200')
    body = {
            'sort':{
                'date':'desc'
                },
            'query':{
                'bool':{
                    'should':[
                        {'term':{'title':search}}
                        ],
                    }
                }
            }
    res = es.search(index='notice', body=body)
    result1 = []
    result2 = []
    result3 = []
    if len(res['hits']['hits']) != 0:
        for hit in res['hits']['hits']:
            result1.append(hit['_source']['date'])
            result2.append(hit['_source']['title'])
            result3.append(hit['_source']['link'])
            msg = '\''+search+'\' 검색 결과입니다.\n\n'
            for i in range(len(result1)):
                msg += str(i+1)+'.\n작성일: '+result1[i]+'\n제목: '+result2[i]+'\n링크: '+result3[i]+'\n\n'
    else:
        msg = '검색 결과가 없습니다.'
    
    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': msg
                    }
                }]
            }
        })
