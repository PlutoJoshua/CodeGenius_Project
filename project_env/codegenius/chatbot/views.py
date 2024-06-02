from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.cache import cache
from django.template.loader import render_to_string
from .models import save_data
import logging
import fasttext
from datetime import datetime

from .classification_model import main as classificate_user_input
from .tasks import (chatting_model_predict, 
                    extract_keyword_user_input)

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
    
    logger.info(f"CHATTING // session email: {request.session.get('email')}")

    ### fasttext classification model setting ###
    classification_model_path = '/app/chatbot/service_model/fasttext_model_v1.bin'
    threshold = 0.7

    ### gpt2 model setting ###

    ### User input ###
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        logger.info(f'USER-INPUT | user input: {user_input}')

    ############################################################################# 파이썬 분류 모델 #############################################################################
        try:
            classification_output = classificate_user_input(
                                                        input_text = user_input, 
                                                        model_path = classification_model_path, 
                                                        threshold = threshold
                                                        )
            logger.info(f'views.py/chatting -> classification successfully')
        
        except Exception as e:
            logger.error(f'views.py/chatting -> Failed to response:classification_model = {email}, input: {user_input}, error: {str(e)}')           
            return HttpResponse('++++++++시스템오류++++++++')

    ######################################################################### gpt2 모델 + keyword 추출 #########################################################################
        try:
            ### 파이썬 관련 질문일 때 ###
            if classification_output == 1:
                try:    
                    ######################## 비동기 작업 ########################
                    chatting_task = chatting_model_predict.delay(user_input)
                    keyword_task = extract_keyword_user_input.delay(user_input)

                    chatting_output = chatting_task.get()
                    keyword_output = keyword_task.get()
                    ############################################################

                    record = save_data.objects.create(
                        email=email,
                        user_input=user_input,
                        chatting_output=chatting_output,
                        keyword=keyword_output.get('keyword', ''),
                        code=keyword_output.get('code', ''),
                        doc_url=keyword_output.get('doc_url', ''),
                        classification_label = 1
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


                except Exception as e:
                    logger.error(f'views.py/chatting/chatting_model_predict -> error: {e}')

            else:
                ### 파이썬 관련 질문이 아닐 때 ###
                ### (email, 질문, classification model result) Database에 저장 ###
                record = save_data.objects.create(
                    email=email,
                    user_input=user_input,
                    classification_label = 0
                )
                return render(request, 'chatting.html', {'chatting_output': '파이썬에 관해 궁금한 점은 없으신가요?'})
        
        except Exception as e:
            logger.error(f'views.py/chatting -> Failed to response: chatbot_model = {email}, input: {user_input}, error: {str(e)}')           
            return HttpResponse('++++++++시스템오류++++++++')

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