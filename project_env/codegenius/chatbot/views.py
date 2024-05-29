from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import save_data
import logging

from .classification_model import classificate_user_input

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
        logger.warning("This is login_view warning - user email is NONE")
        return HttpResponse('서비스를 이용하시려면 로그인이 필요합니다.')
    
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        logger.info(f'user input: {user_input}')
        ### classification 모델을 사용하여 예측값 생성 ###
        try:
            classification_output = classificate_user_input(user_input)
            logger.info(f'classification output: {classification_output}')

            try:
                ### 데이터 저장 ###
                record = save_data(
                    email=email,
                    user_input=user_input,
                    user_output=classification_output
                )
                # 데이터베이스에 저장
                record.save()

            except Exception as e:
                logger.error(f'Failed to save Data -> classification_model: {email}, input: {user_input}, output: {classification_output}, error: {str(e)}')

            return render(request, 'result.html', {'user_output': classification_output})
        
        except Exception as e:
            logger.error(f'Failed to response -> classification_model: {email}, input: {user_input}, error: {str(e)}')
            return HttpResponse('잠시 후 다시 이용해주세요')
        
    else:
        return render(request, 'input_form.html')