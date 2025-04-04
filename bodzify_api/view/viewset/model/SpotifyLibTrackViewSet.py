from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.model.spotify.children.track.Fields import Fields
from bodzify_api.utils.spotify.service import sync_user_spotify_library
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

    @action(detail=False, methods=['post'])
    def sync(self, request):
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
