from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.model.spotify.children.track.Fields import Fields
from bodzify_api.utils.spotify.service import full_sync_spotify_library, quick_sync_spotify_library
from bodzify_api.serializer.model.spotify_lib_track.output.detailed import SpotifyLibTrackDetailedSerializer
from bodzify_api.serializer.model.spotify_lib_track.output.simple import SpotifyLibTrackSimpleSerializer


class SpotifyLibTrackViewSet(ReadOnlyModelViewSet):

    queryset = SpotifyLibTrack.objects.all()
    serializer_class = SpotifyLibTrackSimpleSerializer
    detail_serializer_class = SpotifyLibTrackDetailedSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return self.serializer_class

    def get_queryset(self):
        return super().get_queryset().filter(
            spotify_artists__user=self.request.user,
            **{Fields.IS_REMOVED: False}
        ).distinct()

    @action(detail=False, methods=['post'], url_path='sync/quick')
    def quick_sync(self, request):
        """
        Perform a quick sync of the user's Spotify library.
        This only fetches new additions since the last sync and is faster than a full sync.
        """
        try:
            tracks = quick_sync_spotify_library(request.user)
            return Response(
                {
                    'message': 'Spotify library quick sync completed successfully',
                    'new_tracks_count': len(tracks)
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
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
            full_sync_spotify_library(request.user)
            return Response(
                {'message': 'Spotify library synced successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'])
    def sync(self, request):
        """
        Legacy sync endpoint that performs a full sync.
        Maintained for backwards compatibility.
        """
        try:
            full_sync_spotify_library(request.user)
            return Response(
                {'message': 'Spotify library synced successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
