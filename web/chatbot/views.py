from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def chatting(request):
    return render(request, 'chatting.html')

def history(request):
    return render(request, 'history.html')