#!/usr/bin/env python

from django.urls import include
from django.urls import path
from django.contrib import admin
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from bodzify_api import settings
from bodzify_api.view.viewset.SearchApiViewSet import SearchApiViewSet
from bodzify_api.view.viewset.UserViewSet import UserViewSet
from bodzify_api.view.viewset.TrackViewSet import TrackViewSet
from bodzify_api.view.viewset.ArtistViewSet import ArtistViewSet
from bodzify_api.view.viewset.AlbumViewSet import AlbumViewSet
from bodzify_api.view.viewset.criteria.GenreViewSet import GenreViewSet
from bodzify_api.view.viewset.criteria.TagViewSet import TagViewSet
from bodzify_api.view.viewset.MineTrackViewSet import MineTrackViewSet
from bodzify_api.view.viewset.playlist.PlaylistViewSet import PlaylistViewSet
from bodzify_api.view.viewset.playlist.SimplePlaylistViewSet import SimplePlaylistViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tracks', TrackViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'tags', TagViewSet)
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'mine/tracks', MineTrackViewSet, basename='mine-track')
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'playlists/simple', SimplePlaylistViewSet, basename='simple-playlist')
router.register(r'search', SearchApiViewSet, basename='search')


urlpatterns = [path(settings.API_ROOT_BASE, include(router.urls)),

               path(settings.API_ROOT_BASE + 'admin/', admin.site.urls),

               path(settings.API_ROOT_BASE + 'auth/', include('django.contrib.auth.urls')),
               path(settings.API_ROOT_BASE + 'auth/token/', TokenObtainPairView.as_view(),
                    name='token-obtain-pair'),
               path(settings.API_ROOT_BASE + 'auth/token/refresh/',
                    TokenRefreshView.as_view(), name='token-refresh'),

               path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
               path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(
                   url_name='schema'), name='swagger-ui'),
               path('api/schema/redoc/',
                    SpectacularRedocView.as_view(url_name='schema'), name='redoc')]
