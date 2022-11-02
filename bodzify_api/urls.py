from django.urls import include, path, re_path
from django.contrib import admin

from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import bodzify_api.views as views

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/create/', views.user_create, name='user-create'),
    path('users/<username>/songs/', views.library_song_list, name='library-song-list'),
    path('users/<username>/songs/<songId>/', views.library_song_detail, name='library-song-detail'),
    path('users/<username>/songs/<songId>/download/', 
        views.library_song_download, name='library-song-download'),
    path('mine/songs/', views.mine_song_list, name='mine-song-list'),
    path('mine/songs/download/', views.mine_song_download, name='mine-song-download'),
]
