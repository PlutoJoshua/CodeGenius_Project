from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.cache import cache
from .models import save_data
import logging
import fasttext

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
        logger.info(f'User Logged In: {email}')
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
    
    ### fasttext classification model setting ###
    classification_model_path = '/app/chatbot/service_model/fasttext_model_v1.bin'
    threshold = 0.7

    ### gpt2 model setting ###

    ### User input ###
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        logger.info(f'user input: {user_input}')

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
                    chatting_output = chatting_model_predict.delay(user_input)
                    keyword_output = extract_keyword_user_input.delay(user_input)

                    chatting_result = chatting_output.get()
                    keyword_result = keyword_output.get()
                    ############################################################

                    record = save_data.objects.create(
                        email=email,
                        user_input=user_input,
                        user_output=chatting_result
                    )
                    return render(request, 'chatting.html', {
                                                        'chatting_output': chatting_result, 
                                                        'keyword': keyword_result.get('keyword', ''), 
                                                        'code': keyword_result.get('code', ''), 
                                                        'doc_url': keyword_result.get('doc_url', '')
                                                        }
                                                    )
                except Exception as e:
                    logger.error(f'views.py/chatting/chatting_model_predict -> error: {e}')

            else:
                ### 파이썬 관련 질문이 아닐 때 ###
                ### (email, 질문, classification model result) Database에 저장 ###
                record = save_data.objects.create(
                    email=email,
                    user_input=user_input,
                    user_output=classification_output
                )
                return render(request, 'chatting.html', {'chatting_output': '파이썬에 관한 질문만 해. 사람 화나게하지 말고'})
        
        except Exception as e:
            logger.error(f'views.py/chatting -> Failed to response: chatbot_model = {email}, input: {user_input}, error: {str(e)}')           
            return HttpResponse('++++++++시스템오류++++++++')

    else:
        return render(request, 'chatting.html')

def history(request):
    return render(request, 'history.html')