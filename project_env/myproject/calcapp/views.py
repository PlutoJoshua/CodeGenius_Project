from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Calculation
import logging 
### 로거 생성 ###
logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        ### email을 session에 저장 ###
        request.session['email'] = email  
        ### 로깅 ###
        logger.info(f'User Log In: {email}')
        return redirect('calculate')
    return render(request, 'login.html')

def calculate(request):
    ### session에서 email을 load ###
    email = request.session.get('email')
    if email is None:
        ### calculate page로 바로 접속하여 서비스 이용시 에러 text ### 
        logger.warning("This is login_view warning - user email is NONE")
        return HttpResponse('서비스를 이용하시려면 로그인이 필요합니다.')
    
    if request.method == 'POST':
        input_number = int(request.POST['input_number'])
        calculation = Calculation(input_number=input_number, email=email)
        
        try:
            calculation.calculate_and_save()
            ### 저장 성공 시 로그 ###
            logger.info(f'Calculation performed -> views.calculate: {email}, input: {input_number}, output: {calculation.output_number}')
            return render(request, 'result.html', {'정답': calculation.output_number})
        except Exception as e:
            ### 저장 실패 시 로그 ###
            logger.error(f'Failed to save calculation -> views.calculate: {email}, input: {input_number}, error: {str(e)}')
    
    return render(request, 'calculate.html')