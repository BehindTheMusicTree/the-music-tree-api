from django.urls import include, path, re_path
from django.contrib import admin

from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

import bodzify_api.views as views
from bodzify_api.viewset.LibraryTrackViewSet import LibraryTrackViewSet

router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'tracks', LibraryTrackViewSet, basename='track')

urlpatterns = [
    path('', include(router.urls)),
    
    path('admin/', admin.site.urls),

    path('auth/', include('django.contrib.auth.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/create/', views.user_create, name='user-create'),

    path('users/<username>/library/genres/create/', 
        views.library_genre_create, 
        name='library-genre-create'),
    path('users/<username>/library/genres/', views.library_genre_list, name='library-genre-list'),

    path('mine/tracks/', views.mine_track_list, name='mine-track-list'),
    path('mine/tracks/download/', views.mine_track_download, name='mine-track-download'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', 
        SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
