from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def add_five(number):
    result = number + 5
    # 결과를 로깅
    logger.info(f"add_five 결과: {result}")
    return result

@shared_task
def square(number):
    result = number ** 2
    # 결과를 로깅
    logger.info(f"square 결과: {result}")
    return result