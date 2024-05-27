from django.utils import timezone
from django.db import models
import logging

### 로거 생성 ###
logger = logging.getLogger(__name__)


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
        ### 로깅 ###
        logger.info(f'Calculation performed for email: {self.email}, input: {self.input_number}, output: {self.output_number}')

    class Meta:
        db_table = 'test_io'