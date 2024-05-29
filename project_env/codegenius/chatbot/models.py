from django.db import models
import logging

class Python_classification_model(models.Model):
    ### 유저 email ###
    email = models.EmailField(blank=True, null=True)
    ### 유저 인풋 ###
    user_input = models.CharField(max_length=255)
    ### 유저 아웃풋 ###
    user_output = models.CharField(max_length=255)
    ### 시간 ###
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Input: {self.user_input}, Output: {self.user_output}'

    class Meta:
        db_table = 'test_io'