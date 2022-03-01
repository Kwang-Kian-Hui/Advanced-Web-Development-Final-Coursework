from django.urls import path
from friendchat import views as fcviews
from django.conf.urls.static import static
from django.conf import settings

app_name = "friendchat"

urlpatterns = [
    path('', fcviews.chat_list_view, name="friend_chat_list"),
    path('<friend_id>/', fcviews.chat_view, name='friend_chat'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)