from django.db import models
from .tasks import add_five, square
import logging

logger = logging.getLogger(__name__)

class Calculation(models.Model):
    email = models.EmailField(blank=True, null=True)  
    ### 유저 인풋 ###
    input_number = models.IntegerField()
    ### 유저 아웃풋 ###
    output_number = models.IntegerField(blank=True, null=True)
    ### 비동기 ###
    add_five_result = models.IntegerField(blank=True, null=True)
    square_result = models.IntegerField(blank=True, null=True) 
    ### 시간 ###
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_and_save(self):
        # 계산 수행
        self.output_number = self.input_number * 2 + 1
        self.save()

        # 비동기 작업 호출
        result_add_five = add_five.delay(self.output_number)
        result_square = square.delay(self.output_number)

        # 결과를 저장
        self.save_async_results(result_add_five.get(), result_square.get())

    def save_async_results(self, add_five_result, square_result):
        # 비동기 작업 결과를 저장
        self.add_five_result = add_five_result
        self.square_result = square_result
        self.save()
        
        # 결과를 로깅
        logger.info(f"결과 저장: add_five 결과 - {add_five_result}, square 결과 - {square_result}")

    class Meta:
        db_table = 'test_io'