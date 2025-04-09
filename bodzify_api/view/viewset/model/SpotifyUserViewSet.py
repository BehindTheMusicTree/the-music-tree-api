from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from bodzify_api.model.user.spotify.SpotifyUser import SpotifyUser
from bodzify_api.serializer.model.user.spotify.output.detailed import SpotifyUserDetailedSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.utils.spotify_api.oauth import SpotifyOAuthService
from bodzify_api.utils.spotify_api.lib_track_manager import quick_sync_spotify_lib_tracks, full_sync_spotify_lib_tracks


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

    @extend_schema(
        description="Perform a quick sync of the user's Spotify library. This only fetches new additions since the last sync and is faster than a full sync.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "new_tracks_count": {"type": "integer"}
                }
            },
            409: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
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
    @action(detail=False, methods=['post'], url_path='sync/quick')
    def quick_sync(self, request):
        try:
            with transaction.atomic():
                if request.user.spotify_sync_in_progress:
                    return Response(
                        {'error': 'A sync is already in progress. Please wait for it to complete.'},
                        status=status.HTTP_409_CONFLICT
                    )

                request.user.spotify_sync_in_progress = True
                request.user.save(update_fields=['spotify_sync_in_progress'])

            try:
                tracks = quick_sync_spotify_lib_tracks(request.user)
                return Response(
                    {
                        'message': 'Spotify library quick sync completed successfully',
                        'new_tracks_count': len(tracks)
                    },
                    status=status.HTTP_200_OK
                )
            finally:
                with transaction.atomic():
                    request.user.spotify_sync_in_progress = False
                    request.user.save(update_fields=['spotify_sync_in_progress'])

        except Exception as e:
            with transaction.atomic():
                request.user.spotify_sync_in_progress = False
                request.user.save(update_fields=['spotify_sync_in_progress'])
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        description="Perform a full sync of the user's Spotify library. This checks for both additions and removals, but is more resource-intensive.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            },
            409: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
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
    @action(detail=False, methods=['post'], url_path='sync/full')
    def full_sync(self, request):
        try:
            with transaction.atomic():
                if request.user.spotify_sync_in_progress:
                    return Response(
                        {'error': 'A sync is already in progress. Please wait for it to complete.'},
                        status=status.HTTP_409_CONFLICT
                    )

                request.user.spotify_sync_in_progress = True
                request.user.save(update_fields=['spotify_sync_in_progress'])

            try:
                full_sync_spotify_lib_tracks(request.user)
                return Response(
                    {'message': 'Spotify library synced successfully'},
                    status=status.HTTP_200_OK
                )
            finally:
                with transaction.atomic():
                    request.user.spotify_sync_in_progress = False
                    request.user.save(update_fields=['spotify_sync_in_progress'])

        except Exception as e:
            with transaction.atomic():
                request.user.spotify_sync_in_progress = False
                request.user.save(update_fields=['spotify_sync_in_progress'])
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
