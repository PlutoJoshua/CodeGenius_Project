# Generated by Django 5.0 on 2024-05-31 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='save_data',
            old_name='user_output',
            new_name='chatting_output',
        ),
    ]