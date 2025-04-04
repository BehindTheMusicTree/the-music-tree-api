from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bodzify_api.model.spotify.children.track.SpotifyTrack import SpotifyTrack
from bodzify_api.model.spotify.children.track.Fields import Fields
from bodzify_api.utils.spotify.service import sync_user_spotify_library
from bodzify_api.view.serializer.model.spotify_track.detailed import SpotifyTrackDetailedSerializer
from bodzify_api.view.serializer.model.spotify_track.simple import SpotifyTrackSimpleSerializer


class SpotifyTrackViewSet(ReadOnlyModelViewSet):
    """ViewSet for managing Spotify tracks in the user's library."""

    queryset = SpotifyTrack.objects.all()
    serializer_class = SpotifyTrackSimpleSerializer
    detail_serializer_class = SpotifyTrackDetailedSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return self.serializer_class

    def get_queryset(self):
        """Filter tracks to only show those from the current user's Spotify library."""
        return super().get_queryset().filter(
            spotify_artists__user=self.request.user,
            **{Fields.IS_REMOVED: False}
        ).distinct()

    @action(detail=False, methods=['post'])
    def sync(self, request):
        """Sync the user's Spotify library."""
        try:
            sync_user_spotify_library(request.user)
            return Response(
                {'message': 'Spotify library synced successfully'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
