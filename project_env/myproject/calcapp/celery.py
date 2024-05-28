import os
from celery import Celery

# Django settings를 사용할 수 있도록 환경변수 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Celery 앱 생성
app = Celery('calcapp')

# Celery 설정 로드
app.config_from_object('django.conf:settings', namespace='CELERY')

# 태스크 모듈 로드
app.autodiscover_tasks()