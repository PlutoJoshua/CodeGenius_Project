from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.cache import cache
from .models import save_data
import logging
import fasttext

from .classification_model import main as classificate_user_input

# 로거 생성
logger = logging.getLogger(__name__)

### 로그인 ###
def login_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        ### 이메일을 session에 저장 ###
        request.session['email'] = email
        ### 로깅 ###
        logger.info(f'User Logged In: {email}')
        ### input_form 페이지로 리디렉션 ###
        return redirect('input_form')
    return render(request, 'login.html')

def input_form_view(request):
    ### session에서 email을 load ###
    email = request.session.get('email')
    if email is None:
        ### chat page로 바로 접속하여 서비스 이용시 에러 text ### 
        logger.warning("views.py/input_form_view -> This is login_view warning - user email is NONE")
        return HttpResponse('서비스를 이용하시려면 로그인이 필요합니다.')
    
    classification_model_path = '/app/chatbot/service_model/fasttext_model_v1.bin'

    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        logger.info(f'user input: {user_input}')
        try:
            classification_output = classificate_user_input(
                                                            input_text = user_input, 
                                                            model_path = classification_model_path, 
                                                            threshold = 0.7
                                                            )
            logger.info(f'classification successfully')
            
            # 데이터베이스에 결과 저장
            record = save_data.objects.create(
                email=email,
                user_input=user_input,
                user_output=classification_output
            )
            
            return render(request, 'result.html', {'user_output': classification_output})
        except Exception as e:
            logger.error(f'views.py/input_form_view -> Failed to response:classification_model = {email}, input: {user_input}, error: {str(e)}')
            return HttpResponse('잠시 후 다시 이용해주세요')
        
        return render(request, 'result.html', {'user_output': classification_output, 'probability': probability})
    
    else:
        return render(request, 'input_form.html')