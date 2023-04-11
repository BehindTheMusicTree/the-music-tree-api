#!/usr/bin/env python
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.serializer.track.input.schema.TrackSaveSchemaSerializer import \
    ATTRIBUTES_LABEL as TRACK_SCHEMA_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.input.schema.TrackExtractSchemaSerializer import \
    TrackExtractSchemaSerializer
from bodzify_api.serializer.track.input.schema.TrackExtractSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_EXTRACT_ATTRIBUTE_LABEL
from bodzify_api.serializer.track.input.schema.TrackPostSchemaSerializer import \
    TrackPostSchemaSerializer
from bodzify_api.serializer.track.input.schema.TrackPostSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_POST_ATTRIBUTE_LABEL
from bodzify_api.serializer.track.input.schema.TrackUpdateSchemaSerializer import \
    TrackUpdateSchemaSerializer
from bodzify_api.serializer.track.input.schema.TrackUpdateSchemaSerializer import \
    ATTRIBUTES_LABEL as SCHEMA_UPDATE_ATTRIBUTE_LABEL
from bodzify_api.serializer.track.output.TrackDetailedSerializer import \
    TrackDetailedSerializer
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
import bodzify_api.service.TrackService as TrackService
import bodzify_api.view.utility as utility


class FILTER_FIELDS:
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST_NAME = TRACK_SCHEMA_ATTRIBUTES_LABEL.ARTIST_NAME
    ALBUM_NAME = TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING
    ALBUM_ARTISTS_NAME = TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING
    GENRE_NAME = TRACK_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME
    LANGUAGE = ATTRIBUTES_LABEL.LANGUAGE


class TrackViewSet(MultiSerializerViewSet):

    queryset = LibraryTrack.objects.all()
    serializers = {
        'default': TrackDetailedSerializer,
        'list':  TrackDetailedSerializer,
        'retrieve':  TrackDetailedSerializer,
        'update':  TrackDetailedSerializer,
    }

    def get_queryset(self):
        queryset = LibraryTrack.objects.filter(user=self.request.user)
        titleFilter = self.request.query_params.get(FILTER_FIELDS.TITLE)
        artistNameFilter = self.request.query_params.get(FILTER_FIELDS.ARTIST_NAME)
        albumNameFilter = self.request.query_params.get(FILTER_FIELDS.ALBUM_NAME)
        genreNameFilter = self.request.query_params.get(FILTER_FIELDS.GENRE_NAME)
        languageFilter = self.request.query_params.get(FILTER_FIELDS.LANGUAGE)

        if titleFilter is not None:
            queryset = queryset.filter(title__icontains=titleFilter)
        if artistNameFilter is not None:
            queryset = queryset.filter(
                artist__name__icontains=artistNameFilter)
        if albumNameFilter is not None:
            queryset = queryset.filter(album__name__icontains=albumNameFilter)
        if genreNameFilter is not None:
            queryset = queryset.filter(genre__name__icontain=genreNameFilter)
        if languageFilter is not None:
            queryset = queryset.filter(language__icontains=languageFilter)
        return queryset

    def destroy(self, request, *args, **kwargs):
        self.get_object().deleteWithCheckingAlbumAndArtistPotentialDeletion()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=TrackUpdateSchemaSerializer,
        responses=TrackDetailedSerializer,
        description=("""
            Updates a track:\n"
            - to not update a field, it mustn't be specified (e.g the line \"artistName\":... 
            shouldn't exist). The only exception is the field 'albumArtistsName' (more 
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
               - if it already exists an album with the same name as 'albumName' but with 
            different 'albumArtistsName', an new album is created.\n
               - wether the field 'albumArtistsName' is empty or not specified, it tells that 
            the track's album has no artist.\n
               - if 'albumName' is empty or missing and 'albumArtistsName' is specified, bodzify
            will reject the request.
            """)
    )
    def update(self, request, *args, **kwargs):
        updatedTrack = TrackService.Update(
            user=request.user, updateSchemaData=request.data, oldTrack=self.get_object())
        responseSerializer = TrackDetailedSerializer(updatedTrack)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
            data=TrackDetailedSerializer(updatedTrack).data,
            status=status.HTTP_200_OK,
            headers=headers)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        track = LibraryTrack.objects.get(uuid=pk)
        if track.fileExists:
            return utility.GetFileResponse(filePath=track.file.path, filename=track.file.name)
        else:
            return HttpResponse(
                content="The requested track's file is missing.",
                status=status.HTTP_410_GONE)

    @extend_schema(
        request=TrackPostSchemaSerializer,
        responses=TrackDetailedSerializer,
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
        track = TrackService.Create(
            user=request.user,
            postSchemaData=request.data)
        responseSerializer = TrackDetailedSerializer(track)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
            data=TrackDetailedSerializer(track).data,
            status=status.HTTP_201_CREATED,
            headers=headers)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name=ATTRIBUTES_LABEL.TITLE,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY),
            OpenApiParameter(
                name=ATTRIBUTES_LABEL.ARTIST,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY),
            OpenApiParameter(
                name=TRACK_SCHEMA_ATTRIBUTES_LABEL.ALBUM_ARTISTS_NAME_STRING,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY),
            OpenApiParameter(
                name=TRACK_SCHEMA_ATTRIBUTES_LABEL.GENRE_NAME,
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=TrackExtractSchemaSerializer,
        responses=TrackDetailedSerializer,
        description=("""
            Download a track from the given url to the app. 
            It is done by providing an URL and metadata:
                - "title";
                - "artistName";
                - "albumName";
                - "albumArtistsName";
                - "genreName";
                - "rating";
                - "releasedOn";
                - "language";
                
            The downloaded track's filename will be set as follow:
                - if the "artistName" and "title" fields are provided, the filename will be set to 
                "artistName - title.extension";
                - else if only the title is provided, the filename will be set to "title.extension";
                - else if the title and the artist name are set in the metadata of the track, the 
                filename will be set to "artist name - title.extension";
                - else if only the title is set in the metadata, the filename will be set to 
                "title.extension";
                - else if the length filename of the downloaded track plus de length of the 
                extension s smaller than 100, the filename will be set to "filename.extension";
                - else the filename will be set to "random string.extension".
            """)
    )
    @action(detail=False, methods=['post'])
    def extract(self, request, *args, **kwargs):
        serializer = TrackExtractSchemaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        track = TrackService.Extract(
            user=request.user, extractSchemaData=request.data)
        responseSerializer = TrackDetailedSerializer(track)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
            data=responseSerializer.data, status=status.HTTP_201_CREATED, headers=headers)
