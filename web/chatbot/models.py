from django.db import models

# Create your models here.

class save_data(models.Model):
    ### 유저 email ###
    email = models.EmailField(blank=True, null=True)
    ### 유저 인풋 ###
    user_input = models.CharField(max_length=255)
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
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'django_io'