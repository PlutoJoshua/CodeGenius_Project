from django.apps import AppConfig

class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'
    
    def ready(self):
        # Django 앱이 시작될 때 모델을 로드
        gpt2_path = "/app/chatbot/service_model/kogpt2_chatbot_model.pth"
        load_model(gpt2_path)