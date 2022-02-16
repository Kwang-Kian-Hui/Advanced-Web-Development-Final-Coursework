from django.urls import path
from users import views as uview
from django.conf.urls.static import static
from django.conf import settings

app_name = "users"

urlpatterns = [
    path('<user_id>/', uview.profile_view, name="user_profile"),
    path('<user_id>/edit/', uview.edit_user_view, name="edit_user"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)