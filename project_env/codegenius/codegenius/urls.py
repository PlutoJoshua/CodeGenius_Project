from django.urls import path
from django.contrib import admin
import logging

from chatbot.views import login_view, input_form_view

# 로거 생성
logger = logging.getLogger(__name__)

urlpatterns = [
    path('', login_view, name='login'),  
    path('login/', login_view, name='login'),  # 로그인 페이지
    path('input-form/', input_form_view, name='input_form'),  # 입력 폼 페이지
]

# 로깅 추가
logger.info('URL configuration loaded successfully.')