from django.urls import path
from users import views as uview

app_name = "users"

urlpatterns = [
    path('<username>/', uview.profile_view, name="user_profile"),
    path('<username>/edit/', uview.edit_user_view, name="edit_user"),
]