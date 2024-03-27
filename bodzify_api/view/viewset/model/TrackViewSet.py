#!/usr/bin/env python

import logging

from django.http import HttpResponse
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.serializers import ModelSerializer

import bodzify_api.view.utility as utility
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL as LIB_TRACK_ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackExtractSerializer import LibTrackExtractSerializer
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPostSerializer import LibTrackPostSerializer
from bodzify_api.serializer.track.input.schema.LibTrackSaveSchemaSerializer import FIELDS as SAVE_SCHEMA_FIELDS
from bodzify_api.serializer.track.input.schema.endpoint.LibTrackPutSerializer import LibTrackPutSerializer
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import LibTrackDetailedSerializer
from bodzify_api.service.TrackService import TrackService
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet

logger = logging.getLogger('bodzify_api')


class GET_FILTER_FIELDS:
    TITLE = LIB_TRACK_ATTRIBUTES_LABEL.TITLE
    ARTIST_NAME = SAVE_SCHEMA_FIELDS.ARTIST_NAME
    ALBUM_NAME = SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR
    ALBUM_ARTISTS_NAME = SAVE_SCHEMA_FIELDS.ALBUM_ARTISTS_NAMES_STR
    GENRE_NAME = SAVE_SCHEMA_FIELDS.GENRE_NAME
    LANGUAGE = LIB_TRACK_ATTRIBUTES_LABEL.LANGUAGE


class TrackViewSet(AppModelViewSet):
    queryset = LibraryTrack.objects.all()
    serializers = {
        'default': LibTrackDetailedSerializer,
        'list':  LibTrackDetailedSerializer,
        'retrieve':  LibTrackDetailedSerializer,
        'update':  LibTrackDetailedSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(service=TrackService(), **kwargs)

    def get_queryset(self):
        queryset = LibraryTrack.objects.filter(user=self.request.user)
        title_filter = self.request.GET.get(GET_FILTER_FIELDS.TITLE)
        artist_name_filter = self.request.GET.get(GET_FILTER_FIELDS.ARTIST_NAME)
        album_name_filter = self.request.GET.get(GET_FILTER_FIELDS.ALBUM_NAME)
        genre_name_filter = self.request.GET.get(GET_FILTER_FIELDS.GENRE_NAME)
        language_filter = self.request.GET.get(GET_FILTER_FIELDS.LANGUAGE)

        if title_filter is not None:
            queryset = queryset.filter(title__icontains=title_filter)
        if artist_name_filter is not None:
            queryset = queryset.filter(artist__name__icontains=artist_name_filter)
        if album_name_filter is not None:
            queryset = queryset.filter(album__name__icontains=album_name_filter)
        if genre_name_filter is not None:
            queryset = queryset.filter(genre__name__icontain=genre_name_filter)
        if language_filter is not None:
            queryset = queryset.filter(language__icontains=language_filter)
        return queryset

    def _get_detailed_serializer(self, instance) -> ModelSerializer:
        return LibTrackDetailedSerializer(instance=instance)  # type: ignore

    @extend_schema(parameters=[
        OpenApiParameter(name=GET_FILTER_FIELDS.TITLE, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=GET_FILTER_FIELDS.ARTIST_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name=GET_FILTER_FIELDS.ALBUM_ARTISTS_NAME,
                         type=OpenApiTypes.STR,
                         location=OpenApiParameter.QUERY),
        OpenApiParameter(name=GET_FILTER_FIELDS.GENRE_NAME, type=OpenApiTypes.STR, location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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
        return self._create(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        track = LibraryTrack.objects.get(uuid=pk)
        if track.file_exists:
            return utility.get_file_response(filePath=track.file.path, filename=track.file.name)
        else:
            return HttpResponse(
                content="The requested track's file is missing.",
                status=status.HTTP_410_GONE)

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
        request_data_snake_case = self.get_dict_with_snake_case_keys_from_form_data(request.data)
        serializer = LibTrackExtractSerializer(data=request_data_snake_case)
        serializer.is_valid(raise_exception=True)

        track = self.service.extract(extract_data=request_data_snake_case, request=request)
        response_serializer = LibTrackDetailedSerializer(track)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            data=response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        return self._destroy(request, *args, **kwargs)
