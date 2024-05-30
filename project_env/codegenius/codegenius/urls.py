# from django.contrib import admin
from django.urls import path
import chatbot.views

urlpatterns = [
#    path('admin/', admin.site.urls),
    path('', chatbot.views.homepage, name='homepage'),
    path('chatting/', chatbot.views.chatting, name='chatting'),
    path('history/', chatbot.views.history, name='history'),
]


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)