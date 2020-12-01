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
def waiting_bus(bus):
    msg = []
    now = datetime.datetime.now()
    for i in range(len(bus)):
        bus_time = bus[i]['hour']+'시 '+bus[i]['minute']+'분'
        waiting_time = str(int((timedelta(hours=int(bus[i]['hour']), minutes=int(bus[i]['minute']))-timedelta(hours=now.hour, minutes=now.minute)).seconds/60))+'분 전'
        if now.hour <= int(bus[i]['hour']):
            if now.hour == int(bus[i]['hour']):
                if now.minute < int(bus[i]['minute']):
                    msg.extend([bus_time, waiting_time])
                    return msg
                    
            else:
                msg.extend([bus_time, waiting_time])
                return msg

    msg.append('운행중인 버스가 없습니다.')
    return msg
                
                    

@csrf_exempt
def start_bus(request): 
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer) #카카오톡 내용을 json 포멧으로 받아오기
    return_str = return_json_str['userRequest']['utterance'] # 사용자의 발화만 뽑아냄
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey'] # 유저 식별용으로 받음
    es = Elasticsearch('localhost:9200')
    if datetime.datetime.today().weekday() != 5:
        if datetime.datetime.today().weekday() == 6:
            body1 = {
                '_source':['hour','minute'],
                'size': 200,
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'sunday':True}},
                            {'term':{'departure':'school'}}
                            ]
                        }
                    }
                }
            res1 = es.search(index='bus', body=body1)
            body2 = {
                '_source':['hour','minute'],
                'size': 200,
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'sunday':True}},
                            {'term':{'departure':'station'}}
                            ]
                        }
                    }
                }
            res2 = es.search(index='bus', body=body2)
            bus1=[]
            bus2=[]
            for hit in res1['hits']['hits']:
                bus1.append(hit['_source'])
            for hit in res2['hits']['hits']:
                bus2.append(hit['_source'])

            school = waiting_bus(bus1)
            station = waiting_bus(bus2)
        else:
            body1 = {
                '_source':['hour','minute'],
                'size': 200,
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'departure':'school'}}
                            ],
                        'must_not':[
                            {'term':{'sunday':True}}
                            ]
                        }
                    }
                }
            res1 = es.search(index='bus', body=body1)
            body2 = {
                '_source':['hour','minute'],
                'size': 200,
                'query':{
                    'bool':{
                        'must':[
                            {'term':{'departure':'station'}}
                            ],
                        'must_not':[
                            {'term':{'sunday':True}}
                            ]
                        }
                    }
                }
            res2 = es.search(index='bus', body=body2)
            bus1=[]
            bus2=[]
            for hit in res1['hits']['hits']:
                bus1.append(hit['_source'])
            for hit in res2['hits']['hits']:
                bus2.append(hit['_source'])
            
            school = waiting_bus(bus1)
            station = waiting_bus(bus2)
        
        if len(school)==2:
            msg = school[0]+'에 학교에서 출발\n'+'('+school[1]+')\n'
        else:
            msg = '학교에서 출발: '+school[0]+'\n'

        if len(station)==2:
            msg = msg + station[0]+'에 조치원역 뒤에서 출발\n'+'('+station[1]+')'
        else:
            msg = msg + '조치원역 뒤에서 출발: '+station[0]+'\n'
        return JsonResponse({
            'version': '2.0',
            'data': {
                'test1': msg
            }
        })
    else:
        return JsonResponse({
            'version': '2.0',
            'data': {
                'test1': '토요일에는 운행을 하지 않습니다.'
            }
        })

@csrf_exempt
def bab(request):
    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{                                               
                'basicCard': {
                    'description': '아래 버튼을 눌러 이번 주 메뉴를 확인하세요.',
                    'buttons': [
                        {
                            'action': 'webLink',
                            'label': '식단표 확인하기',
                            'webLinkUrl': 'http://sejong.korea.ac.kr/dext5editordata/20201130_102304640_36322.jpg'
                        }]
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
    #bab_link = weekly_menu.objects.last()


    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': user_info
                        }
                }]
            }
        })



