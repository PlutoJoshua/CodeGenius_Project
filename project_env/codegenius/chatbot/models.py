from django.db import models
import logging

logger = logging.getLogger(__name__)

class save_data(models.Model):
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

    def save(self, *args, **kwargs):

        logger.info(f'Saving model instance: email={self.email}, user_input={self.user_input}, user_output={self.user_output}')
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'test_io'