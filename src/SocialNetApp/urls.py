"""SocialNetApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from base import views as bviews
from users import views as uviews
from userposts import views as upviews


urlpatterns = [
    # path('', bviews.home_page, name='home'),
    path('', upviews.home_page, name='home'),
    path('admin/', admin.site.urls),
    path('chat/', include('friendchat.urls')),
    path('friend/', include('friends.urls', namespace="friends")),
    path('login/', uviews.login_view, name="login"),
    path('logout/', uviews.logout_view, name="logout"),
    path('profile/', include('users.urls', namespace="profile")),
    path('register/', uviews.registration_view, name="register"),
    path('search/', uviews.user_search_view, name="search"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)