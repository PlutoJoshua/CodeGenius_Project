from django.utils import timezone
from django.db import models

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
    
    class Meta:
        db_table = 'test_io'