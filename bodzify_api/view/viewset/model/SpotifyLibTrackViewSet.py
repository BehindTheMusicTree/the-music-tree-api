from drf_spectacular.utils import OpenApiParameter  # type: ignore
from drf_spectacular.types import OpenApiTypes  # type: ignore
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from bodzify_api.filtering.set.spotify.lib_track.SpotifyLibTrackFilterSet import SpotifyLibTrackFilterSet
from bodzify_api.filtering.set.spotify.lib_track.Fields import Fields as FilterFields
from bodzify_api.model.spotify_resource.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.model.spotify_resource.children.track.Fields import Fields
from bodzify_api.utils.spotify_api import lib_track_manager as spotify_api_lib_track_manager
from bodzify_api.serializer.model.spotify.lib_track.output.detailed import SpotifyLibTrackDetailedSerializer
from bodzify_api.serializer.model.spotify.lib_track.output.simple import SpotifyLibTrackSimpleSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class SpotifyLibTrackViewSet(AppModelViewSet[SpotifyLibTrack]):
    def __init__(self, **kwargs):
        super().__init__(model_class=SpotifyLibTrack,
                         filterset_class=SpotifyLibTrackFilterSet,
                         detailed_serializer_class=SpotifyLibTrackDetailedSerializer,
                         simple_serializer_class=SpotifyLibTrackSimpleSerializer,
                         is_private_resource=False,
                         **kwargs)

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return super().get_queryset().none()
        return super().get_queryset().filter(
            **{Fields.IS_REMOVED: False}
        ).distinct()

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ALBUM_ARTIST_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.DURATION_SEC_MIN, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.DURATION_SEC_MAX, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.POPULARITY_MIN, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.POPULARITY_MAX, type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.EXPLICIT, type=OpenApiTypes.BOOL, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.LAST_SYNCED_AT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.LAST_SYNCED_AT_GT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.LAST_SYNCED_AT_LT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.LAST_SYNCED_AT_GTE, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.LAST_SYNCED_AT_LTE, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.IS_REMOVED, type=OpenApiTypes.BOOL, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.CREATED_ON, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.CREATED_ON_GT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.CREATED_ON_LT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.CREATED_ON_GTE, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.CREATED_ON_LTE, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.UPDATED_ON, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.UPDATED_ON_GT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.UPDATED_ON_LT, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.UPDATED_ON_GTE, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.UPDATED_ON_LTE, type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY),
    ])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    @action(detail=False, methods=['post'], url_path='sync/quick')
    def quick_sync(self, request):
        """
        Perform a quick sync of the user's Spotify library.
        This only fetches new additions since the last sync and is faster than a full sync.
        """
        try:
            with transaction.atomic():
                # Check if a sync is already in progress
                if request.user.spotify_sync_in_progress:
                    return Response(
                        {'error': 'A sync is already in progress. Please wait for it to complete.'},
                        status=status.HTTP_409_CONFLICT
                    )

                # Mark sync as in progress
                request.user.spotify_sync_in_progress = True
                request.user.save(update_fields=['spotify_sync_in_progress'])

            try:
                tracks = spotify_api_lib_track_manager.quick_sync_spotify_lib_tracks(request.user)
                return Response(
                    {
                        'message': 'Spotify library quick sync completed successfully',
                        'new_tracks_count': len(tracks)
                    },
                    status=status.HTTP_200_OK
                )
            finally:
                # Reset sync status
                with transaction.atomic():
                    request.user.spotify_sync_in_progress = False
                    request.user.save(update_fields=['spotify_sync_in_progress'])

        except Exception as e:
            # Ensure sync status is reset even if an error occurs
            with transaction.atomic():
                request.user.spotify_sync_in_progress = False
                request.user.save(update_fields=['spotify_sync_in_progress'])
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='sync/full')
    def full_sync(self, request):
        """
        Perform a full sync of the user's Spotify library.
        This checks for both additions and removals, but is more resource-intensive.
        """
        try:
            with transaction.atomic():
                # Check if a sync is already in progress
                if request.user.spotify_sync_in_progress:
                    return Response(
                        {'error': 'A sync is already in progress. Please wait for it to complete.'},
                        status=status.HTTP_409_CONFLICT
                    )

                # Mark sync as in progress
                request.user.spotify_sync_in_progress = True
                request.user.save(update_fields=['spotify_sync_in_progress'])

            try:
                spotify_api_lib_track_manager.full_sync_spotify_lib_tracks(request.user)
                return Response(
                    {'message': 'Spotify library synced successfully'},
                    status=status.HTTP_200_OK
                )
            finally:
                # Reset sync status
                with transaction.atomic():
                    request.user.spotify_sync_in_progress = False
                    request.user.save(update_fields=['spotify_sync_in_progress'])

        except Exception as e:
            # Ensure sync status is reset even if an error occurs
            with transaction.atomic():
                request.user.spotify_sync_in_progress = False
                request.user.save(update_fields=['spotify_sync_in_progress'])
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
