from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from plan.models import Plan
import datetime
from datetime import timedelta
from django.db.models import Count
# Create your views here.
@csrf_exempt
def show_plan(count, plan_db): # 일정 확인 텍스트부분
    if count==0:
        msg = '일정이 없어요.'
        return msg
    else:
        msg = '일정이 ' + str(count) + '개 있습니다.\n'
        for i in range(count):
            tmp = plan_db[i]
            msg += str(i+1) + '.\n' + '장소:' + tmp.place + '\n내용:' + tmp.content + '\n'
        return msg

@csrf_exempt
def start_plan(request): # 일정 시작
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer) #카카오톡 내용을 json 포멧으로 받아오기
    return_str = return_json_str['userRequest']['utterance'] # 사용자의 발화만 뽑아냄
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey'] # 유저 식별용으로 받음
    now = datetime.date.today()
    plan_db = Plan.objects.filter(date = now, user = user_info)
    plan_count = plan_db.count()
    
    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'basicCard': {
                    'description': '오늘 ' + show_plan(plan_count, plan_db), #일정 있을 때와 없을 때를 구분하기 위함
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
                        },
                        {
                            'label': '일정 수정/삭제',
                            'action': 'message',
                            'messageText': '일정 수정/삭제'
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
def message(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey'] 
    return_act = return_json_str['action']['detailParams'] 
    date = return_act['date']['origin']
    place = return_act['place']['value']
    content = return_act['content']['value']
    
    if return_str == '일정 등록':
        Plan(user=user_info, date=date, place=place, content=content).save()
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': '일시:' + date + '\n' + '장소:' + place + '\n' + '내용:' + content +
                                '\n일정을 잘 저장했어요!',
                        'buttons': [
                            {
                                'label': '일정 수정',
                                'action': 'message',
                                'messageText': '등록 중 일정 수정'
                            },
                            {
                                'label': '취소',
                                'action': 'message',
                                'messageText': '등록 중 일정 삭제'
                            }]
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
    plan_db = Plan.objects.filter(date = date, user = user_info)
    plan_count = plan_db.count()

    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'basicCard': {
                    'description': '선택하신 날짜('+str(date)+')의 '+show_plan(plan_count, plan_db)
                    }
                }]
            }
        })

@csrf_exempt
def check_plan_date(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    plan_db = Plan.objects.values('date').annotate(total=Count('date')).order_by('date')
    msg = ''
    for i in range(len(plan_db)):
        msg = msg + str(plan_db[i]['date']) + ' : ' + str(plan_db[i]['total']) + '개\n'
    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'basicCard': {
                    'description':'일정이 총 '+ str(len(plan_db))+'개 있어요.\n'+msg
                    }
                }]
            }
        })


@csrf_exempt
def change_plan(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    ch_date = return_act['ch_date']['origin']
    ch_place = return_act['ch_place']['origin']
    ch_content = return_act['ch_content']['origin']
    recent_plan = Plan.objects.filter(user=user_info).last()
    recent_plan.delete()
    Plan(user=user_info, date=ch_date, place=ch_place, content=ch_content).save()
    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                        'text': ch_date + '\n' + ch_place + '\n' + ch_content + '\n일정 수정 완료!'
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
def delete_plan(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    msg=''

    if return_str == '등록 중 일정 삭제':
        recent_plan = Plan.objects.filter(user=user_info).last()
        recent_plan.delete()
        ch_date = return_act['ch_date']['origin']
        ch_place = return_act['ch_place']['origin']
        ch_content = return_act['ch_content']['origin']
        msg = '일시:' + str(ch_date) + '\n장소:' + ch_place + '\n시간:' + ch_content + '\n\n해당 일정 등록을 취소했습니다.'
    else:
        msg = '미완'
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
    plan_db = Plan.objects.filter(user=user_info)
    #plan_db_last = plan_db.last()
    now = datetime.date.today()   
    #plan_db_last.delete()
    dic = Plan.objects.values('date').annotate(total=Count('date')).order_by('date')
    #a = dic.date
    #b = dic.total
    #.annotate(total=Count('date')).order_by('date')
    #msg = msg+'일정 존재하는 날짜는 총 '+dic_count+'일'+'\n'
    
    info = []
    for obj in dic:
        info.append([ obj['date'], obj['total'] ])

    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': str(info)  #오늘 일정 1개 삭제완료'
                        }
                }]
            }
        })



