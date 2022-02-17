from django.urls import path
from friends import views as fviews

app_name = "friend"

urlpatterns = [
    path('friend_request/', fviews.send_friend_request, name="friend_request"),
    path('friend_request/<user_id>/', fviews.friend_request_view, name="friend_request_list"),
]