from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from .models import save_data
import logging

from .chatting_model import chatting_model  # 예측 함수
from .extrack_keyword import extrack_keyword  # 쿼리 함수

logger = logging.getLogger(__name__)

@shared_task
def chatting_model_predict(user_input):
    try:
        # user_input을 사용하여 모델 예측
        result = chatting_model(user_input)
        return result
        
    except Exception as e:
        logger.error(f'tasks.py/chatting_model_predict -> Error: {e}')
        return ' '

@shared_task
def extract_keyword_user_input(user_input):
    try:
        # user_input을 사용하여 데이터베이스 쿼리
        result = extrack_keyword(user_input)
        return result

    except ObjectDoesNotExist:
        logger.error(f'tasks.py/extract_keyword_user_input -> error: No matching record found')
        return {}

    except Exception as e:
        logger.error(f'tasks.py/extract_keyword_user_input -> Error: {e}')
        return {}