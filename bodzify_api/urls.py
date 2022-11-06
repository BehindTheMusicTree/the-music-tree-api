from django.urls import include, path
from django.contrib import admin

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from bodzify_api.viewset.UserViewSet import UserViewSet
from bodzify_api.viewset.LibraryTrackViewSet import LibraryTrackViewSet
from bodzify_api.viewset.GenreViewSet import GenreViewSet
from bodzify_api.viewset.MineTrackViewSet import MineTrackViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tracks', LibraryTrackViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'mine/tracks', MineTrackViewSet, 'mine-track')

base = 'api/v1/'

urlpatterns = [
    path(base, include(router.urls)),
    
    path(base + 'admin/', admin.site.urls),

    path(base + 'auth/', include('django.contrib.auth.urls')),
    path(base + 'auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(base + 'auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', 
        SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
