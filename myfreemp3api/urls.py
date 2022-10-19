from django.urls import include, path, re_path
from django.contrib import admin

from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('songs/', views.song_list, name='song-list'),
    path('songs/<int:pk>/', views.song_detail, name='song-detail'),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/create/', views.UserCreationView),
    path('external/songs/', views.external_song_list, name='external-song-list'),
    path('external/songs/download/', views.external_song_download, name='external-song-download'),
]
