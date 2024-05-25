from django.utils import timezone
from django.db import models

import logging
from .logging import DatabaseHandler

### Logger 설정 (debug level) ###
logger = logging.getLogger('calcapp')
logger.setLevel(logging.DEBUG)

### DatabaseHandler를 로거에 추가 ###
db_handler = DatabaseHandler()
logger.addHandler(db_handler)

class Calculation(models.Model):
    ### views.py에서 전달 받은 email ###
    email = models.EmailField(blank=True, null=True)  
    input_number = models.IntegerField()
    output_number = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_and_save(self):
        self.output_number = self.input_number * 2 + 1
        self.save()

        ### 모델 사용 후 로그 기록 ###
        logger.info(f'Calculation performed for email: {self.email}, input: {self.input_number}, output: {self.output_number}')
    
    class Meta:
        db_table = 'test_io'