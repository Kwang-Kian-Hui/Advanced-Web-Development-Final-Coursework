from django.urls import path
from users import views as uview
from django.conf.urls.static import static
from django.conf import settings
from . import api

app_name = "user_app"

urlpatterns = [
    path('<user_id>/', uview.profile_view, name="user_profile"),
    path('<user_id>/edit/', uview.edit_user_view, name="edit_user"),
    path('api/user/', api.CreateUser.as_view(), name='create_user_api'), 
    path('api/user/<int:pk>/', api.UserDetail.as_view(), name='user_detail_api'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)