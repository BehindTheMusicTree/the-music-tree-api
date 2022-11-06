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

base = 'api/' + r'^(?P<version>(v1))/'

urlpatterns = [
    re_path(base, include(router.urls)),
    
    re_path(base + 'admin/', admin.site.urls),

    re_path(base + 'auth/', include('django.contrib.auth.urls')),
    re_path(base + 'auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(base + 'auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    re_path(base + 'users/create/', views.user_create, name='user-create'),

    re_path(base + 'mine/tracks/download/', views.mine_track_download, name='mine-track-download'),

    path(base + 'api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', 
        SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
