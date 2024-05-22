from django.shortcuts import render
from django.http import HttpResponse
from .models import Calculation

def calculate(request):
    if request.method == 'POST':
        input_number = int(request.POST['input_number'])
        calculation = Calculation(input_number=input_number)
        calculation.calculate_and_save()
        return HttpResponse(f'Result: {calculation.output_number}')
    return render(request, 'calculate.html')