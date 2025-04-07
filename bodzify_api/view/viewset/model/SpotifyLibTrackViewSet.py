from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db import transaction

from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.model.spotify.children.track.Fields import Fields
from bodzify_api.utils.spotify.service import full_sync_spotify_library, quick_sync_spotify_library
from bodzify_api.serializer.model.spotify_lib_track.output.detailed import SpotifyLibTrackDetailedSerializer


class SpotifyLibTrackViewSet(ModelViewSet):

    queryset = SpotifyLibTrack.objects.all()
    serializer_class = SpotifyLibTrackDetailedSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return super().get_queryset().none()
        return super().get_queryset().filter(
            **{Fields.IS_REMOVED: False}
        ).distinct()

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
                tracks = quick_sync_spotify_library(request.user)
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
                full_sync_spotify_library(request.user)
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
