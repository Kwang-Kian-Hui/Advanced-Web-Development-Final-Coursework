from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from friendchats import views as fcviews

app_name = "friendchat_app"

urlpatterns = [
    path('<chat_room_id/', fcviews.chatroom_view, name="chat_room"),
    path('chat_list/<user_id>', fcviews.chatroom_list_view, name="chat_list"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)