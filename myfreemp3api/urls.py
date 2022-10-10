from django.urls import include, path
from django.contrib import admin

from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from myfreemp3api.api import views

import logging


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'songs', views.SongDBViewSet, basename='song')

logger = logging.getLogger('info')
logger.info("router")
logger.info(str(router.urls))
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/create/', views.UserCreationView),
    path('external/songs/', views.ExternalSongsView.as_view()),
    path('external/songs/download/', views.ExternalSongDownloadView.as_view()),
]

logger.info("patterns")
logger.info(str(urlpatterns))
