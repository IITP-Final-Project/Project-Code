from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

@csrf_exempt
def message(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer) #카카오톡 내용을 json 포멧으로 받아오기
    return_str = return_json_str['userRequest']['utterance'] # 사용자의 발화만 뽑아냄
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey'] # 유저 식별용으로 받음
    return_act = return_json_str['action']['detailParams'] # 파라미터 설정에 따라 전달되는 부분
    day = return_act['day']['value'] # day 파라미터의 내용 가져오기
    subject = return_act['subject']['value']
    time = return_act['time']['origin']
    prof = return_act['prof']['value']


    if return_str == '시간표 등록':
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'basicCard': {
                        'description': day + '\n' + subject + '\n' + time + '\n' + prof +
                                '\n시간표 저장 완료! (db연동 필요)',
                        'buttons': [
                            {
                                'label': '시간표 수정',
                                'action': 'message',
                                'messageText': '등록 중 시간표 수정'
                            },
                            {
                                'label': '취소',
                                'action': 'message',
                                'messageText': '시간표 삭제'
                            }]
                }}]
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
def change_timetable(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']
    return_act = return_json_str['action']['detailParams']
    ch_day = return_act['ch_day']['value']
    ch_subject = return_act['ch_subject']['origin']
    ch_time = return_act['ch_time']['origin']
    ch_prof = return_act['ch_prof']['origin']

    return JsonResponse({
        'version': '2.0',
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': ch_day + '\n' + ch_subject + '\n' + ch_time + '\n' + ch_prof + '\n시간표 수정 완료!(db연동 필요)'
                }
            }],
            'quickReplies': [{
                'label': '처음으로',
                'action': 'message',
                'messageText': '처음으로'
            }]
        }
    })          
