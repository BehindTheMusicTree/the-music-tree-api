from django.urls import include, path
from django.contrib import admin

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from bodzify_api.view.viewset.UserViewSet import UserViewSet
from bodzify_api.view.viewset.track.LibraryTrackViewSet import LibraryTrackViewSet
from bodzify_api.view.viewset.criteria.GenreViewSet import GenreViewSet
from bodzify_api.view.viewset.criteria.TagViewSet import TagViewSet
from bodzify_api.view.viewset.track.MineTrackViewSet import MineTrackViewSet
from bodzify_api.view.viewset.playlist.PlaylistViewSet import PlaylistViewSet
from bodzify_api.view.LogoutView import LogoutView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tracks', LibraryTrackViewSet)
router.register(r'tags/', TagViewSet)
router.register(r'genres/', GenreViewSet)
router.register(r'mine/tracks', MineTrackViewSet, 'mine-track')
router.register(r'playlists', PlaylistViewSet)
#router.register(r'playlists/zoomable/', PlaylistViewSet)
#router.register(r'tagplaylists', TagPlaylistViewSet)

base = 'api/v1/'

urlpatterns = [
    path(base, include(router.urls)),
    
    path(base + 'admin/', admin.site.urls),

    path(base + 'auth/', include('django.contrib.auth.urls')),
    path(base + 'auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path(base + 'auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path(base + 'auth/logout/', LogoutView.as_view(), name='auth-logout'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', 
        SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
