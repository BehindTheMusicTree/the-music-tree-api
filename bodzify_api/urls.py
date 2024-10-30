#!/usr/bin/env python

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from bodzify_api import settings
from bodzify_api.view.viewset.model.AlbumViewSet import AlbumViewSet
from bodzify_api.view.viewset.model.ArtistViewSet import ArtistViewSet
from bodzify_api.view.viewset.model.criteria.GenreViewSet import GenreViewSet
from bodzify_api.view.viewset.model.criteria.TagViewSet import TagViewSet
from bodzify_api.view.viewset.model.playlist.GenrePlaylistViewSet import GenrePlaylistViewSet
from bodzify_api.view.viewset.model.playlist.PlaylistViewSet import PlaylistViewSet
from bodzify_api.view.viewset.model.playlist.ManualPlaylistViewSet import ManualPlaylistViewSet
from bodzify_api.view.viewset.model.PlayViewSet import PlayViewSet
from bodzify_api.view.viewset.model.TrackViewSet import TrackViewSet
from bodzify_api.view.viewset.model.UserViewSet import UserViewSet
from bodzify_api.view.viewset.SearchApiViewSet import SearchApiViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tracks', TrackViewSet, basename='library-track')
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'plays', PlayViewSet, basename='play')

# Do not move PlaylistViewSet after GenrePlaylistViewSet or ManualPlaylistViewSet or it will cause confusion resolving
# reverse urls.
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'manual-playlists', ManualPlaylistViewSet, basename='manual-playlist')
router.register(r'genre-playlists', GenrePlaylistViewSet, basename='genre-playlist')
router.register(r'search', SearchApiViewSet, basename='search')

urlpatterns = [path(settings.API_ROOT_BASE, include(router.urls)),

               path(settings.API_ROOT_BASE + 'admin/', admin.site.urls),

               path(settings.API_ROOT_BASE + 'auth/', include('django.contrib.auth.urls')),
               path(settings.API_ROOT_BASE + 'auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
               path(settings.API_ROOT_BASE + 'auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

               path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
               path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
               path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')]


if settings.STATIC_FILES_STATE in [settings.StaticFileState.COLLECTING, settings.StaticFileState.SERVING]:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
