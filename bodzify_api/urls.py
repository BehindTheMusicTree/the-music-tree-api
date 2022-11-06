from django.urls import include, path, re_path
from django.contrib import admin

from rest_framework import routers

import logging

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

import bodzify_api.views as views
from bodzify_api.viewset.LibraryTrackViewSet import LibraryTrackViewSet
from bodzify_api.viewset.GenreViewSet import GenreViewSet

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'tracks', LibraryTrackViewSet)
router.register(r'genres', GenreViewSet)

logger = logging.getLogger('info')
logger.info('DOIHDOIUHDODIUHPDOIHUDPOIDHPDIUHDPIUHPIUDHDPIHUDPIDUHPDIUH')
base = 'api/' + r'^(?P<version>(v1))/'

urlpatterns = [
    path(base, include(router.urls)),
    
    path('admin/', admin.site.urls),

    path('auth/', include('django.contrib.auth.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/create/', views.user_create, name='user-create'),

    path('mine/tracks/download/', views.mine_track_download, name='mine-track-download'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', 
        SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
