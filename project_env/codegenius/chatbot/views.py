import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.cache import cache
from django.template.loader import render_to_string
from .models import save_data, Label_0_answer
import logging
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
    api_key = "AIzaSyAOBGlVPR_uefBsR01G6HJZ7oQ69-nDGSo"
    ### gpt2 model setting ###
    gpt2_path = "/app/chatbot/service_model/kogpt2_chatbot_model.pth"

    ### User input ###
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        if user_input == None:
            logger.warning(f'USER-INPUT | user input is {user_input}!!!!!')
            logger.warning(f"CHATTING // session email: {request.session.get('email')}")
            classification_output = "no"
        else:    
            logger.info(f'USER-INPUT | user input: {user_input}')
            logger.info(f"CHATTING // session email: {request.session.get('email')}")

    ########################################################################## gpt2 + fasttext ##########################################################################
            tasks = group(
                classification_model_predict.s(
                    user_input = user_input, 
                    api_key = api_key
                    ), 
                chatting_model_predict.s(
                    user_input = user_input,
                    model_path = gpt2_path
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
            random_num = random.randint(0, 9)
            record = Label_0_answer.objects.get(id=random_num)
            answer = record.answer

            return render(request, 'chatting.html', {'chatting_output': answer})
        

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