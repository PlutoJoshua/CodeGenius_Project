from django.db import models

class Calculation(models.Model):
    input_number = models.IntegerField()
    output_number = models.IntegerField(blank=True, null=True)

    def calculate_and_save(self):
        self.output_number = self.input_number * 2 + 1
        self.save()
    
    class Meta:
        db_table = 'test_io'