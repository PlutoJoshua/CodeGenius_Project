from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.core.cache import cache
from django.template.loader import render_to_string
from .models import save_data
from datetime import datetime
from itertools import groupby

# Create your views here.
def homepage(request):

    save_datas = save_data.objects.all()

    if request.method == 'POST':
        email = request.POST['email']
        ### 이메일을 session에 저장 ###
        request.session['email'] = email
        ### chatting 페이지로 리디렉션 ###
        print(f'HOMEPAGE // User Logged In: {email}')
        return redirect('chatting')
    
    return render(request, 'homepage.html', {'save_datas': save_datas})


def history(request):
    email = request.session.get('email', '이메일이 설정되지 않았습니다.')
    print(email)
    #################### history.html 렌더링 ####################
    ### created_at 기준 내림차순 정렬, email = email ###
    user_records = save_data.objects.filter(email=request.session.get('email')).order_by('-created_at')

    history_data = []

    for created_at, group in groupby(user_records, key=lambda x: x.created_at.strftime('%Y-%m-%d')):
        temp_data = []

        for record in group:
            temp_data.append({
                'user_input': record.user_input,
                'chatting_output': record.chatting_output,
                'keyword': record.keyword,
                'doc_url': record.doc_url,
            })

        history_data.append({
            'created_at': created_at,
            'records': temp_data
        })

    # history.html 템플릿을 렌더링
    # rendered_html = render_to_string('history.html', {'history_records': user_records, 'user_email': email, 'history_data' : history_data})

    return render(request, 'history.html', {'history_records': user_records, 'user_email': email, 'history_data' : history_data})
    
    # history_return = {
    #     'history_json': history_data,
    #     'rendered_html' : rendered_html,
    # }

    # return JsonResponse(history_return)


def history_render(request):
    return render(request, 'history_render.html')


def chatting(request):
    ### session에서 email을 load ###
    email = request.session.get('email', '이메일이 설정되지 않았습니다.')

    ### User input ###
    if request.method == 'POST':
        user_input = request.POST['user_input']
        print(user_input)

        classification_output = 1

        ### 파이썬 관련 질문일 때 ###
        if classification_output == 1:

            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            #################### chatting.html 렌더링 ####################
            chatting_html = render_to_string('chatting.html', {
                'chatting_output': 'chatting_output',
                'keyword': 'keyword', 
                'code': 'code', 
                'doc_url': 'doc_url',
                'current_time': current_time
            })
            return HttpResponse(chatting_html)

        else:
            return render(request, 'chatting.html', {'chatting_output': '파이썬에 관해 궁금한 점은 없으신가요?'})
    else:
        return render(request, 'chatting.html')