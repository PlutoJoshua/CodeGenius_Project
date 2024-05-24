from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Calculation

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        ### email을 session에 저장 ###
        request.session['email'] = email  
        return redirect('calculate')
    return render(request, 'login.html')

def calculate(request):
    ### session에서 email을 load ###
    email = request.session.get('email')
    if email is None:
        ### calculate page로 바로 접속하여 서비스 이용시 에러 text ### 
        return HttpResponse('서비스를 이용하시려면 로그인이 필요합니다.')
    
    if request.method == 'POST':
        input_number = int(request.POST['input_number'])
        calculation = Calculation(input_number=input_number, email=email)
        calculation.calculate_and_save()
        return render(request, 'result.html', {'정답': calculation.output_number})
    return render(request, 'calculate.html')