from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.
def keyboard(request):
    return JsonResponse({
        'type':'buttons',
        'buttons':['버튼1','버튼2']
    })

@csrf_exempt
def message(request):
    answer = ((request.body).decode('utf-8'))
    return_json_str = json.loads(answer)
    return_str = return_json_str['userRequest']['utterance']
    user_info = return_json_str['userRequest']['user']['properties']['plusfriendUserKey']

    if return_str == '테스트':
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': '당신의 user key는 {} 입니다.'.format(user_info)
                    }
                }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action': 'message',
                    'messageText': '처음으로'
                }]
            }
        })

    elif return_str == '테스트2':
        return JsonResponse({
            'version': '2.0',
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': '테스트2입니다.'
                    }
                }]
            }
        })

