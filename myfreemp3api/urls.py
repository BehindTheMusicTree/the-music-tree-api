from django.urls import include, path

from rest_framework import routers
from rest_framework.authtoken import views as authtoken_views

from myfreemp3api.api import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/login', authtoken_views.obtain_auth_token),
    path('users', include('django.contrib.auth.urls')),
    path('users/create', views.UserCreationView),

    path('songs/', views.SongView)
]
