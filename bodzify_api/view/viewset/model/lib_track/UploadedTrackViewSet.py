import os
from drf_spectacular.types import OpenApiTypes  # type: ignore
from drf_spectacular.utils import OpenApiParameter, extend_schema  # type: ignore
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from bodzify_api.filtering.set.lib_track.LibTrackFilterSet import UploadedTrackFilterSet
from bodzify_api.model.lib_track.LibTrack import UploadedTrack
from bodzify_api.model.lib_track.Fields import Fields
from bodzify_api.view.serializer.model.uploaded_track.detailed import UploadedTrackDetailedSerializer
from bodzify_api.view.serializer.model.uploaded_track.post import UploadedTrackPostSerializer
from bodzify_api.view.serializer.model.uploaded_track.put import UploadedTrackPutSerializer
from bodzify_api.view.serializer.model.uploaded_track.simple import UploadedTrackSimpleSerializer
from bodzify_api.view.viewset.base.BaseViewSet import BaseViewSet


class UploadedTrackViewSet(BaseViewSet):
    """ViewSet for managing uploaded tracks."""

    queryset = UploadedTrack.objects.all()
    serializer_class = UploadedTrackSimpleSerializer
    filterset_class = UploadedTrackFilterSet

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UploadedTrackDetailedSerializer
        elif self.action == 'create':
            return UploadedTrackPostSerializer
        elif self.action in ['update', 'partial_update']:
            return UploadedTrackPutSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download the track file."""
        track = self.get_object()
        return Response({
            Fields.FILE_PATH: track.file_path
        }, status=status.HTTP_200_OK)

    @extend_schema(request=UploadedTrackPostSerializer, responses=UploadedTrackDetailedSerializer, description=("""
        Create a track with metadata by uploading or a file or downloading it from another source:
            # Uploading a file:
                - if the file has no metadata 'title', it is set with the file's name without the extension (with an 
                random identifier if another track has the same filename);
            # Downloading a file:
                It is done by providing an URL and metadata (title, artist's name, album's name, album's artists' names,
                genre's name, rating, releasedOn, language etc.).
                    
                The downloaded track's filename will be set as follow:
                    - if the "artist_name" and "title" fields are provided, the filename will be set to 
                    "artist_name - title.extension";
                    - else if only the title is provided, the filename will be set to "title.extension";
                    - else if the title and the artist name are set in the metadata of the track, the filename will be set 
                    to "artist name - title.extension";
                    - else if only the title is set in the metadata, the filename will be set to "title.extension";
                    - else if the length filename of the downloaded track plus de length of the extension s smaller than 
                    100, the filename will be set to "filename.extension";
                    - else the filename will be set to "random string.extension".
            # File's metadata:
                - some media players allow to edit tags (e.g the title, the artist's name, the rating etc.). In some cases, 
            the tag isn't store in the file's metadata but in the database of the player. In these cases, the tag won't 
            be imported into the app and will be set to null (= no value). It is the case for:
                    - iTunes' tracks' rating;
                    - Windows Media Player's wav and flac files tags;
                    - Winamp's wav files rating;
                    - Traktor's wav files tags;
        """)
                   )
    def create(self, request, *args, **kwargs):
        try:
            return self._handle_post(request)
        except Exception as e:
            # Clean up temporary file if it exists
            if request.FILES.get(
                    PostFields.TRACK_FILE_PUBLIC) and hasattr(
                    request.FILES[PostFields.TRACK_FILE_PUBLIC],
                    'temporary_file_path'):
                try:
                    os.unlink(request.FILES[PostFields.TRACK_FILE_PUBLIC].temporary_file_path())
                except (OSError, AttributeError):
                    pass  # Ignore cleanup errors
            raise  # Re-raise the original exception

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.TITLE, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ARTISTS_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ALBUM_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.GENRE_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.LANGUAGE, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()

    @extend_schema(request=UploadedTrackPutSerializer,
                   responses=UploadedTrackDetailedSerializer,
                   description=("""
            Updates a track:\n"
            - to not update a field, it mustn't be specified (e.g the line \"artist_name\":... 
            shouldn't exist). The only exception is the field 'album_artists_name' (more precisions below).\n
            - to empty a field (artist or album), the field should be specified with an empty string.\n
            - updating the rating will delete all the ratins from other media players like Windows Media Player or
            MusicBee (iTunes doesn't write rating in the files); 
            - if the album or the artist is updated, the old artist/album is checked to lookup if it is still linked to 
            something: \n
               - for an album, if no track is linked, it is deleted;\n
               - for an artist, if no track and no album is linked, it is deleted. An artist can have no track linked to 
               it if only it is still linked to an album of a track 
            still in the library. E.g: a user only have one track in his library: 'Jamming' by Bob Marley and The 
            Wailers'. The album artists are 'Bob Marley' and 'The Wailers'. 
            The artist 'Bob Marley' is still in the library even if it has no track which has the artist 'Bob Marley'.
            \n\n"
            - as two albums can share the same name (e.g from two different artists), the mean the system to identify an 
            album is the peer (album'sname/album's artists'names). 
            Thus:\n" +
               - if it already exists an album with the same name as 'album_name' but with different 
               'album_artists_name', an new album is created.\n
               - wether the field 'album_artists_name' is empty or not specified, it tells that the track's album has no 
               artist.\n
               - if 'album_name' is empty or missing and 'album_artists_name' is specified, bodzify will reject the 
               request.
            """))
    def update(self, request, *args, **kwargs):
        return self._handle_update(request)

    def destroy(self, *args, **kwargs):
        return self._handle_destroy()
