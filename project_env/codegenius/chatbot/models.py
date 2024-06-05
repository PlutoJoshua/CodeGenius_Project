from django.db import models
import logging

logger = logging.getLogger(__name__)

class save_data(models.Model):
    ### 유저 email ###
    email = models.EmailField(blank=True, null=True)
    ### 유저 인풋 ###
    user_input = models.CharField(max_length=255, null=True)
    ### 채팅 아웃풋 ###
    chatting_output = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=255, blank=True, null=True)
    doc_url = models.CharField(max_length=255, blank=True, null=True)
    classification_label = models.CharField(max_length=10, blank=True, null=True)
    ### 시간 ###
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Input: {self.user_input}, Output: {self.chatting_output}'

    def save(self, *args, **kwargs):

        logger.info(f'Saving model instance: email={self.email}, user_input={self.user_input}, chatting_output={self.chatting_output}')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'django_io'


class Label_0_answer(models.Model):
    # 필드 정의
    answer = models.CharField(max_length=255)

    def __str__(self):
        return self.answer
    
    class Meta:
        db_table = 'label_0_answer'
        managed = False