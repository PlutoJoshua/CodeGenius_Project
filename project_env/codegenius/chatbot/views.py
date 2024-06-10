import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from django.core.exceptions import ObjectDoesNotExist
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
        data = json.loads(request.body.decode('utf-8'))
        user_input = data.get('user_input')

        if not user_input:
            logger.warning(f'USER-INPUT | user input is {user_input}!!!!!')
            logger.warning(f"CHATTING // session email: {email}")
            classification_output = "no"
        else:
            logger.info(f'USER-INPUT | user input: {user_input}')
            logger.info(f"CHATTING // session email: {email}")

            # gpt2 + fasttext
            ######################################### 비동기 작업 #########################################
            chatting_task = chatting_model_predict.apply_async(args=(user_input, gpt2_path))

            classification_task = classification_model_predict.apply_async(args=(user_input, api_key))
            ##############################################################################################

            classification_output = classification_task.get(timeout=5)

                # 분류에 따라 query 작업
            if classification_output == "yes":

                try:    

                    chatting_output = chatting_task.get(timeout=20)
                        
                except Exception as e:
                    logger.error(f'views.py/chatting/chatting_model_predict -> error: {e}')
                    chatting_output = "죄송합니다, 답변을 생성하는데 문제가 발생했습니다."
                
                try:

                    keyword_output = extrack_keyword(user_input)

                except ObjectDoesNotExist:
                    logger.error(f'views.py/extrack_keyword -> error: No matching record found')
                    keyword_output = {'keyword': '', 'code': '', 'doc_url': ''}
                except Exception as e:
                    logger.error(f'views.py/extrack_keyword -> Error: {e}')
                    keyword_output = {'keyword': '', 'code': '', 'doc_url': ''}

                record = save_data.objects.create(
                    email=email,
                    user_input=user_input,
                    chatting_output=chatting_output,
                    keyword=keyword_output.get('keyword', ''),
                    code=keyword_output.get('code', ''),
                    doc_url=keyword_output.get('doc_url', ''),
                    classification_label=classification_output
                )

                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # chatting.html 렌더링
                chatting_html = {
                    'chatting_output': chatting_output,
                    'keyword': keyword_output.get('keyword', ''),
                    'code': keyword_output.get('code', ''),
                    'doc_url': keyword_output.get('doc_url', ''),
                    'current_time': current_time
                }
                return JsonResponse(chatting_html)

            else:
                # 파이썬 관련 질문이 아닐 때
                random_num = random.randint(0, 9)
                record = Label_0_answer.objects.get(id=random_num)
                answer = record.answer

                record = save_data.objects.create(
                    email=email,
                    user_input=user_input,
                    chatting_output=answer,
                    classification_label=classification_output
                )

                return JsonResponse({'chatting_output': answer})

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

    history_data = []
    for record in history_records:
        history_data.append({
            'user_input': record.user_input,
            'chatting_output': record.chatting_output,
            'keyword': record.keyword,
            'code': record.code,
            'doc_url': record.doc_url,
            'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return JsonResponse({'history_records': history_data})