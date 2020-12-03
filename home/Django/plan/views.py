from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from datetime import timedelta
from django.db.models import Count
import re
from elasticsearch import Elasticsearch


# Create your views here.
@csrf_exempt
def show_plan(count, plan_db): # 일정 확인 텍스트부분
    if count==0:
        msg = '일정이 없어요.'
        return msg
    else:
        msg = '일정이 ' + str(count) + '개 있습니다.\n\n'
        result1 = []
        result2 = []
        for hit in plan_db:
            result1.append(hit['_source']['place'])
            result2.append(hit['_source']['subject'])
        for i in range(len(result1)):
            msg += str(i+1) + '.\n장소:' + result1[i] + '\n\n내용:' + result2[i] + '\n\n' 
        return msg

@csrf_exempt
def start_plan(request): # 일정 시작
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer) #카카오톡 내용을 json 포멧으로 받아오기
    return_str = return_json_str['userRequest']['utterance'] # 사용자의 발화만 뽑아냄
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey'] # 유저 식별용으로 받음
    now = datetime.date.today()
    es = Elasticsearch('localhost:9200')
    body = {
            'size':20,
            'query':{
                'bool':{
                    'must':[
                        {'term':{'deadline':now}},
                        {'term':{'userID':user_info}}
                        ],
                    }
                }
            }
    res = es.search(index='schedule', body=body)
    plan_db = res['hits']['hits']
    plan_count = len(plan_db)

    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'basicCard': {
                    'description': '오늘 ' + show_plan(plan_count, plan_db)+'\n\n일정 수정/삭제는 조회 후 가능합니다.', #일정 있을 때와 없을 때를 구분하기 위함
                    'buttons': [
                        {
                            'label': '일정 등록',
                            'action': 'message',
                            'messageText': '일정 등록'
                        },
                        {
                            'label': '일정 조회',
                            'action': 'message',
                            'messageText': '일정 조회'
                        }]
                }}],
            'quickReplies': [
                {
                    'label': '처음으로',
                    'action': 'message',
                    'messageText': '처음으로'
                }]
        }
    })


@csrf_exempt
def message(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey'] 
    return_act = return_json_str['action']['detailParams'] 
    date = return_act['date']['origin']
    place = return_act['place']['origin']
    content = return_act['content']['origin']
    if return_str == '일정 등록':
        es = Elasticsearch('localhost:9200')
        body={'userID': user_info, 'subject': content, 'deadline': date, 'place': place}
        es.index(index='schedule', body=body)
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': '일시:' + date + '\n\n' + '장소:' + place + '\n\n' + '내용:' + content +
                                '\n\n일정을 잘 저장했어요!'
                    }}],
                'quickReplies': [{
                        'label': '처음으로',
                        'action': 'message',
                        'messageText': '처음으로'
                }]
            }
        })
   
    else:
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': '알 수 없는 요청입니다. 처음으로 돌아가주세요.'
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
def check_plan(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    date = return_act['select_date']['origin']
    es = Elasticsearch('localhost:9200')
    body = {
        'size':20,
        'query':{
            'bool':{
                'must':[
                    {'term':{'deadline':date}},
                    {'term':{'userID':user_info}}
                    ],
                }
            }
        }
    res = es.search(index='schedule', body=body)
    plan_db = res['hits']['hits']
    plan_count = len(plan_db)
    
    if plan_count != 0:
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': '선택하신 날짜('+str(date)+')의 '+show_plan(plan_count, plan_db)
                        }
                    }],
                'quickReplies': [
                    {
                        'label': '일정 수정',
                        'action': 'message',
                        'messageText': '조회 후 일정 수정'
                    },
                    {
                        'label': '일정 삭제',
                        'action': 'message',
                        'messageText': '조회 후 일정 삭제'
                    },
                    {
                        'label': '처음으로',
                        'action': 'message',
                        'messageText': '처음으로'
                    }]
         }
        })
    else:
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': '선택하신 날짜('+str(date)+')의 '+show_plan(plan_count, plan_db)
                        }
                    }],
                'quickReplies': [
                    {
                        'label': '처음으로',
                        'action': 'message',
                        'messageText': '처음으로'
                    }]
            }})

@csrf_exempt
def check_plan_date(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    es = Elasticsearch('localhost:9200')
    body = {
        'size':0,
        'query':{
            'bool':{
                'must':[
                    {'term':{'userID':user_info}}
                    ]
                }
            },
        'aggs':{
            'date_his':{
                'terms':{
                    'field':'deadline'
                    }
                }
            }
        }
    res = es.search(index='schedule', body=body)
    all_plan = res['hits']['total']['value']
    plan_db = res['aggregations']['date_his']['buckets']
    result1 = []
    result2 = []
    for hit in plan_db:
        result1.append(hit['key_as_string'])
        result2.append(hit['doc_count'])
        msg = ''
        for i in range(len(result1)):
            msg = msg + str(result1[i]) + ' : ' + str(result2[i]) + '개\n\n'
    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'basicCard': {
                    'description':'일정이 총 '+ str(all_plan)+'개 있어요.\n\n'+msg,
                    'buttons': [
                        {
                            'label': '상세조회',
                            'action': 'message',
                            'messageText': '일정 상세조회'
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
def select_change_plan(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    date = return_act['date']['origin']
    num = return_act['num']['origin']
    input_num = re.findall("\d+", num)
    plan_num = int(input_num[0])-1
    es = Elasticsearch('localhost:9200')
    body = {
            'query':{
                'bool':{
                    'must':[
                        {'term':{'deadline':date}},
                        {'term':{'userID': user_info}}
                        ]
                    }
                }
            }
    res = es.search(index='schedule',body=body)
    doc_id = res['hits']['hits'][plan_num]['_id']
    doc_source = res['hits']['hits'][plan_num]['_source']	
    if return_str == '조회 후 날짜 수정':
        ch_date = return_act['ch_date']['origin']
        doc_source['deadline'] = ch_date
        es.index(index='schedule', id=doc_id, body=doc_source)
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': '날짜 : '+str(doc_source['deadline'])+'\n\n장소 : '+doc_source['place']+'\n\n내용 : '+doc_source['subject'] + '\n\n일정 수정완료!'
                        }
                }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action':'message',
                    'messageText': '처음으로'
                }]
            }
        })
    elif return_str == '조회 후 장소 수정':
        ch_place = return_act['ch_place']['origin']
        doc_source['place'] = ch_place
        es.index(index='schedule', id=doc_id, body=doc_source)
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': '날짜 : '+str(doc_source['deadline'])+'\n\n장소 : '+doc_source['place']+'\n\n내용 : '+doc_source['subject'] + '\n\n>일정 수정완료!'
                        }
                    }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action':'message',
                    'messageText': '처음으로'
                    }]
                }
            })
    elif return_str == '조회 후 내용 수정':
        ch_content = return_act['ch_content']['origin']
        doc_source['subject'] = ch_content
        es.index(index='schedule', id=doc_id, body=doc_source)
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': '날짜 : '+str(doc_source['deadline'])+'\n\n장소 : '+doc_source['place']+'\n\n내용 : '+doc_source['subject'] + '\n\n>일정 수정완료!'
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
def choose_change_plan(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    date = return_act['date']['origin']
    num = return_act['num']['origin']
    input_num = re.findall("\d+", num)
    if len(input_num) == 0:
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard':{
                        'description': '숫자만 입력 가능합니다. 다시 조회해주세요.',
                        'buttons': [
                            {
                                'label': '돌아가기',
                                'action': 'message',
                                'messageText': '일정 상세조회'
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
    
    else:
        plan_num = int(input_num[0])-1
        es = Elasticsearch('localhost:9200')
        body = {
            'query':{
                'bool':{
                    'must':[
                        {'term':{'deadline':date}},
                        {'term':{'userID': user_info}}
                        ]
                    }
                }
            }
        res = es.search(index='schedule',body=body)
        doc_source = res['hits']['hits'][plan_num]['_source']
        plan_count = len(res['hits']['hits'])
        if int(input_num[0]) > plan_count:
            return JsonResponse({
                'version': '2.0',
                'template': {
                    'outputs': [{
                        'basicCard': {
                            'description': '잘못된 번호를 입력하셨습니다.',
                            'buttons': [
                                {
                                    'label': '돌아가기',
                                    'action': 'message',
                                    'messageText': '일정 상세조회'
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
    if return_str == '조회 후 일정 수정':
        if int(input_num[0]) <= plan_count:
            msg = '선택하신 일정입니다. \n\n' + '날짜 : '+str(doc_source['deadline'])+'\n\n장소 : '+doc_source['place']+'\n\n내용 : '+doc_source['subject'] + '\n\n수정할 항목을 선택해주세요.'
            return JsonResponse({
                'version': '2.0',
                'template': {
                    'outputs': [{
                        'basicCard': {
                            'description': msg,
                            'buttons': [
                                {
                                        'label': '날짜',
                                        'action': 'message',
                                        'messageText': '조회 후 날짜 수정'
                                },
                                {
                                        'label': '장소',
                                        'action': 'message',
                                        'messageText': '조회 후 장소 수정'
                                },
                                {
                                        'label': '내용',
                                        'action': 'message',
                                        'messageText': '조회 후 내용 수정'
                                }]
                        }}],
                    'quickReplies': [{
                        'label': '처음으로',
                        'action': 'message',
                        'messageText': '처음으로'
                    }]
                }
            })
    elif return_str == '조회 후 일정 삭제':
        if int(input_num[0]) <= plan_count:
            msg = '선택하신 일정입니다. \n\n' + '날짜 : '+str(doc_source['deadline'])+'\n\n장소 : '+doc_source['place']+'\n\n내용 : '+doc_source['subject']
            return JsonResponse({
                'version': '2.0',
                'template': {
                    'outputs': [{
                        'basicCard': {
                            'description': msg,
                            'buttons': [
                                {
                                    'label': '삭제',
                                    'action': 'message',
                                    'messageText': '선택한 일정 삭제'
                                    },
                                {
                                    'label': '돌아가기',
                                    'action': 'message',
                                    'messageText': '일정 상세조회'
                                    }]
                                }}],
                        'quickReplies': [{
                            'label': '처음으로',
                            'action': 'message',
                            'messageText': '처음으로'
                            }]
                        }
                })

@csrf_exempt
def select_delete_plan(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    date = return_act['date']['origin']
    num = return_act['num']['origin']
    input_num = re.findall("\d+", num)
    plan_num = int(input_num[0])-1
    es = Elasticsearch('localhost:9200')
    body = {
        'query':{
            'bool':{
                'must':[
                    {'term':{'deadline':date}},
                    {'term':{'userID': user_info}}
                    ]
                }
            }
        }
    res = es.search(index='schedule',body=body)
    doc_id = res['hits']['hits'][plan_num]['_id']
    es.delete(index='schedule', id=doc_id)
    return JsonResponse({
        'version': '2.0',                        
        'template': {             
            'outputs': [{
                'simpleText': {
                    'text': '해당 일정을 삭제했습니다.'
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
    return_act = return_json_str['action']['detailParams']
    search = return_act['search']['origin']
#    plan_db = Plan2.objects.filter(date = now, user = user_info)
#    a=Plan2.objects.all()
#    plan_db_count = len(plan_db)
#    plan_db_last = plan_db[len(plan_db)-1]
#    plan_db_last.delete()




    es = Elasticsearch('localhost:9200')

    index = 'lecture_rate'
    search_field = 'context'
    body = {"query":
            {"match":
                {search_field: search  #"context": search
                    }
                }
            }

    res = es.search(index=index, body=body)
    
    result = []
    for hit in res['hits']['hits']:
        result.append(hit['_source']['context'])
    msg = '\''+search+'\' 검색 결과입니다.\n\n'
    for i in range(len(result)):
        msg += str(i+1)+'. '+result[i]+'\n\n'

    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': msg  #'test'
                        }
                }]
            }
        })



