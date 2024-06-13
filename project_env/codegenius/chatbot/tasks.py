from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from .models import save_data
import logging

from .chatting_model import chatting_model, load_model
from .classification_model import Google_gemini as classificate_user_input 

logger = logging.getLogger(__name__)

@shared_task
def load_model_task():
    load_model()
    logger.info('tasks.py/load_model_task -> Model loaded successfully.')

@shared_task
def chatting_model_predict(user_input, model_path):
    response = chatting_model(user_input, model_path)
    return response


@shared_task
def classification_model_predict(user_input, api_key):

    classification_output = classificate_user_input(
        user_input = user_input, 
        api_key = api_key
        )
    return classification_output