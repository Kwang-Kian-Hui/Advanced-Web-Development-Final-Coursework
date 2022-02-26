from django.urls import path, include
from friendchat import views as fcviews

app_name = "friendchat"

urlpatterns = [
    path('<friend_id>/', fcviews.chat_view, name='friend_chat')
]