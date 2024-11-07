from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import settings
from .view.viewset.model.AlbumViewSet import AlbumViewSet
from .view.viewset.model.ArtistViewSet import ArtistViewSet
from .view.viewset.model.criteria.children.GenreViewSet import GenreViewSet
from .view.viewset.model.criteria.children.TagViewSet import TagViewSet
from .view.viewset.model.playlist.PlaylistViewSet import PlaylistViewSet
from .view.viewset.model.playlist.children.GenrePlaylistViewSet import GenrePlaylistViewSet
from .view.viewset.model.playlist.children.ManualPlaylistViewSet import ManualPlaylistViewSet
from .view.viewset.model.PlayViewSet import PlayViewSet
from .view.viewset.model.TrackViewSet import LibTrackViewSet
from .view.viewset.model.UserViewSet import UserViewSet
from .view.viewset.SearchApiViewSet import SearchApiViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tracks', LibTrackViewSet, basename='library-track')
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
