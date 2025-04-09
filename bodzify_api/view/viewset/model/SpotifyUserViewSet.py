from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from bodzify_api.model.user.spotify.SpotifyUser import SpotifyUser
from bodzify_api.serializer.model.user.spotify.output.detailed import SpotifyUserDetailedSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.utils.spotify_api.oauth import SpotifyOAuthService


class SpotifyUserViewSet(AppModelViewSet[SpotifyUser]):
    def __init__(self, **kwargs):
        super().__init__(
            model_class=SpotifyUser,
            detailed_serializer_class=SpotifyUserDetailedSerializer,
            is_private_resource=False,
            is_pk_uuid=False,
            **kwargs
        )

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return super().get_queryset().none()
        return super().get_queryset().filter(id=self.request.user.id)

    @extend_schema(
        description="Get the current user's Spotify profile",
        responses={
            200: SpotifyUserDetailedSerializer,
            401: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                }
            },
            404: {
                "type": "object",
                "properties": {
                    "detail": {"type": "string"}
                }
            }
        }
    )
    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    @extend_schema(
        description="Refresh the Spotify access token using the refresh token",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "expires_in": {"type": "integer"}
                }
            },
            500: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                }
            }
        }
    )
    @action(detail=False, methods=['post'], url_path='refresh-token')
    def refresh_token(self, request):
        try:
            oauth_service = SpotifyOAuthService()
            token_info = oauth_service.refresh_access_token(request.user.spotify_refresh_token)

            request.user.spotify_access_token = token_info['access_token']
            request.user.spotify_token_expires_at = timezone.now(
            ) + timezone.timedelta(seconds=token_info['expires_in'])
            request.user.save()

            return Response({
                'message': 'Token refreshed successfully',
                'expires_in': token_info['expires_in']
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
