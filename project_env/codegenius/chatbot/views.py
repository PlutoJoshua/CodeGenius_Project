from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.cache import cache
from django.template.loader import render_to_string
from .models import save_data
import logging
import fasttext
from datetime import datetime

from celery import Celery, group

from .extrack_keyword import extrack_keyword
from .tasks import (chatting_model_predict, 
                    classification_model_predict)

# 로거 생성
logger = logging.getLogger(__name__)

def homepage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        ### 이메일을 session에 저장 ###
        request.session['email'] = email
        logger.info(f'HOMEPAGE // User Logged In: {email}')
        ### chatting 페이지로 리디렉션 ###
        return redirect('chatting')    

    return render(request, 'homepage.html')

def chatting(request):
    ### session에서 email을 load ###
    email = request.session.get('email')
    if email is None:
    ### chatting page로 바로 접속하여 서비스 이용시 에러 log ### 
        logger.warning("views.py/chatting -> This is login_view warning - user email is NONE")
        return redirect('homepage')  
    
    ### gemini classification model setting ###
    api_key = "AIzaSyCLmV2CGmQRyqRlfysRuW1XzOB-2c_Yd44"
    ### gpt2 model setting ###


    ### User input ###
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        logger.info(f'USER-INPUT | user input: {user_input}')
        logger.info(f"CHATTING // session email: {request.session.get('email')}")

    ########################################################################## gpt2 + fasttext ##########################################################################
        tasks = group(
            classification_model_predict.s(
                user_input = user_input, 
                api_key = api_key
                ), 
            chatting_model_predict.s(
                user_input
                )
            ).apply_async()

        classification_output = tasks.get()[0]

    ######################################################################## 분류에 따라 query작업 ########################################################################
        ### gtp2와 fasttext 동시진행 ###
        ### fasttext 값에 따라 gpt2 모델 값 대기 선택 ###

        ### 파이썬 관련 질문일 때 ###
        if classification_output == "yes":
            try:    

                keyword_output = extrack_keyword(user_input)

            except ObjectDoesNotExist:
                logger.error(f'views.py/extrack_keyword -> error: No matching record found')
            except Exception as e:
                logger.error(f'views.py/extrack_keyword -> Error: {e}')

            try:

                chatting_output = tasks.get()[1]
            
            except Exception as e:
                logger.error(f'views.py/chatting/chatting_model_predict -> error: {e}')


            record = save_data.objects.create(
                email=email,
                user_input=user_input,
                chatting_output=chatting_output,
                keyword=keyword_output.get('keyword', ''),
                code=keyword_output.get('code', ''),
                doc_url=keyword_output.get('doc_url', ''),
                classification_label = classification_output
            )

            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            #################### chatting.html 렌더링 ####################
            chatting_html = render_to_string('chatting.html', {
                'chatting_output': chatting_output, 
                'keyword': keyword_output.get('keyword', ''), 
                'code': keyword_output.get('code', ''), 
                'doc_url': keyword_output.get('doc_url', ''),
                'current_time': current_time
            })


            return HttpResponse(chatting_html)


        else:
            ### 파이썬 관련 질문이 아닐 때 ###
            ### (email, 질문, classification model result) Database에 저장 ###
            record = save_data.objects.create(
                email=email,
                user_input=user_input,
                classification_label = classification_output
            )
            return render(request, 'chatting.html', {'chatting_output': '파이썬에 관해 궁금한 점은 없으신가요?'})
        

    else:
        return render(request, 'chatting.html')

def history(request):
    email = request.session.get('email')
    if email is None:
    ### chatting page로 바로 접속하여 서비스 이용시 에러 log ### 
        logger.warning("views.py/history -> This is login_view warning - user email is NONE")
        return redirect('homepage')  

    logger.info(f"HISTORY // session email: {request.session.get('email')}")
    
    #################### history.html 렌더링 ####################
    ### created_at 기준 내림차순 정렬, email = email ###
    history_records = save_data.objects.filter(email=request.session.get('email')).exclude(chatting_output=0).order_by('-created_at')

    # history.html에 history_records 전달
    return render(request, 'history.html', {'history_records': history_records})