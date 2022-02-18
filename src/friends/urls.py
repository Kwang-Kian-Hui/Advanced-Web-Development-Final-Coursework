from django.urls import path
from friends import views as fviews

app_name = "friend_app"

urlpatterns = [
    path('accept_friend_request/<friend_request_id>/', fviews.accept_friend_request, name="accept_friend_request"),
    path('friend_request/', fviews.send_friend_request, name="friend_request"),
    path('friend_request/<user_id>/', fviews.friend_request_view, name="friend_request_list"),
    path('remove_friend/', fviews.remove_friend, name="remove_friend"),
]