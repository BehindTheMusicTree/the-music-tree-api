
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # type: ignore
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from bodzify_api.serializer.schema.track.input.endpoint.extract import LibTrackExtractSerializer
from bodzify_api.serializer.schema.track.input.endpoint.post import LibTrackPostSerializer
from bodzify_api.serializer.schema.track.input.endpoint.put import LibTrackPutSerializer
from bodzify_api.view import utils
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.service.TrackService import TrackService
from bodzify_api.serializer.schema.track.output.detailed import LibTrackDetailedSerializer
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.filter.set.LibTrackFilterSet import LibTrackFilterSet, Fields as FilterFields


class LibTrackViewSet(AppModelViewSet):
    def __init__(self, **kwargs):
        super().__init__(
            service=TrackService(),
            model_class=LibraryTrack,
            filter_class=LibTrackFilterSet,
            detailed_serializer_class=LibTrackDetailedSerializer,
            **kwargs
        )

    def _get_create_serializer_class_eventually_depending_on_action(self):
        if self.action == 'create':
            return LibTrackPostSerializer
        elif self.action == 'extract':
            return LibTrackExtractSerializer
        raise NotImplementedError(f"No serializer defined for action {self.action}")

    def _post_depending_on_action(self, request, request_data_validated):
        try:
            if self.action == 'create':
                return self._create(request, request_data_validated)
            elif self.action == 'extract':
                track_service: TrackService = self.service  # type: ignore
                return track_service.extract(extract_data_validated=request_data_validated, request=request)
        except OSError as e:
            if e.errno == 28:  # No space left on device
                return Response(data={"detail": "No space left on device."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                raise  # Re-raise the exception if it's not the specific error

    def _create(self, request, request_data_snake_case):
        track_service: TrackService = self.service  # type: ignore
        return track_service.post(post_data_validated=request_data_snake_case, request=request)

    @extend_schema(parameters=[
        OpenApiParameter(name=FilterFields.TITLE, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ARTISTS_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.ALBUM_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.GENRE_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=FilterFields.LANGUAGE, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ])
    def list(self, request, *args, **kwargs):
        return super()._list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(request=LibTrackPostSerializer,
                   responses=LibTrackDetailedSerializer,
                   description=(
                       """
        Create a track with metadata by uploading a file:
            - if the file has no metadata 'title', it is set with the file's name without the 
        extension (with an identifier if another track has the same name);
            - some media players allow to edit tags (e.g the title, the artist's name, the rating 
            etc.). In some cases, the tag isn't store in the file's metadata but in the 
            database of the player. In those cases, the tag won't be imported into Bodzify and 
            will be set to null (= no value). 
            rating). It is the case for:
                - iTunes' tracks' rating;
                - Windows Media Player's wav and flac files tags;
                - Winamp's wav files rating;
                - Traktor's wav files tags;
        """)
                   )
    def create(self, request, *args, **kwargs):
        return self._post(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        track: LibraryTrack = LibraryTrack.objects.get(uuid=pk)
        return utils.get_file_response(filePath=track.track_file.file.path, filename=track.track_file.file.name)

    @transaction.atomic
    @extend_schema(request=LibTrackExtractSerializer,
                   responses=LibTrackDetailedSerializer,
                   description=("""
            Download a track from the given url to the app. 
            It is done by providing an URL and metadata:
                - "title";
                - "artist_name";
                - "album_name";
                - "album_artists_name_string";
                - "genre_name";
                - "rating";
                - "releasedOn";
                - "language";
                
            The downloaded track's filename will be set as follow:
                - if the "artist_name" and "title" fields are provided, the filename will be set to 
                "artist_name - title.extension";
                - else if only the title is provided, the filename will be set to "title.extension";
                - else if the title and the artist name are set in the metadata of the track, the 
                filename will be set to "artist name - title.extension";
                - else if only the title is set in the metadata, the filename will be set to 
                "title.extension";
                - else if the length filename of the downloaded track plus de length of the 
                extension s smaller than 100, the filename will be set to "filename.extension";
                - else the filename will be set to "random string.extension".
            """))
    @action(detail=False, methods=['post'])
    def extract(self, request, *args, **kwargs):
        return self._post(request, *args, **kwargs)

    @transaction.atomic
    @extend_schema(request=LibTrackPutSerializer,
                   responses=LibTrackDetailedSerializer,
                   description=("""
            Updates a track:\n"
            - to not update a field, it mustn't be specified (e.g the line \"artist_name\":... 
            shouldn't exist). The only exception is the field 'album_artists_name' (more 
            precisions below).\n
            - to empty a field (artist or album), the field should be specified with an empty 
            string.\n
            - updating the rating will delete all the ratins from other media players like 
            Windows Media Player or MusicBee (iTunes doesn't write rating in the files); 
            - if the album or the artist is updated, the old artist/album is checked to lookup 
            if it is still linked to something: \n
               - for an album, if no track is linked, it is deleted;\n
               - for an artist, if no track and no album is linked, it is deleted. An artist 
            can have no track linked to it if only it is still linked to an album of a track 
            still in the library. E.g: a user only have one track in his library: 'Jamming' by
            Bob Marley and The Wailers'. The album artists are 'Bob Marley' and 'The Wailers'. 
            The artist 'Bob Marley' is still in the library even if it has no track which has 
            the artist 'Bob Marley'.\n\n" +
            - as two albums can share the same name (e.g from two different artists), the mean 
            the system to identify an album is the peer (album'sname/album's artists'names). 
            Thus:\n" +
               - if it already exists an album with the same name as 'album_name' but with 
            different 'album_artists_name', an new album is created.\n
               - wether the field 'album_artists_name' is empty or not specified, it tells that 
            the track's album has no artist.\n
               - if 'album_name' is empty or missing and 'album_artists_name' is specified, bodzify
            will reject the request.
            """)
                   )
    def update(self, request, *args, **kwargs):
        return self._update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self._destroy(request, *args, **kwargs)
