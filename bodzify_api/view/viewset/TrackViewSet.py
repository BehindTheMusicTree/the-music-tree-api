#!/usr/bin/env python
import pprint
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.serializer.track.input.TrackPostSchemaSerializer import TrackPostSchemaSerializer
from bodzify_api.serializer.track.output.TrackDetailedSerializer import TrackDetailedSerializer
from bodzify_api.serializer.track.input.TrackUpdateSchemaSerializer import TrackUpdateSchemaSerializer
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
import bodzify_api.service.TrackService as TrackService
import bodzify_api.view.utility as utility

FILTER_TITLE_PARAMETER_NAME = LibraryTrack.ATTRIBUTE_TITLE_LABEL
FILTER_ARTIST_NAME_PARAMETER_NAME = TrackUpdateSchemaSerializer.ATTRIBUTE_ARTIST_NAME_LABEL
FILTER_ALBUM_NAME_PARAMETER_NAME = TrackUpdateSchemaSerializer.ATTRIBUTE_ALBUM_NAME_LABEL
FILTER_ALBUM_ARTISTS_NAME_PARAMETER_NAME = (
    TrackUpdateSchemaSerializer.ATTRIBUTE_ALBUM_ARTISTS_NAMES_LABEL)
FILTER_GENRE_NAME_PARAMETER_NAME = TrackUpdateSchemaSerializer.ATTRIBUTE_GENRE_NAME_LABEL
FILTER_LANGUAGE_PARAMETER_NAME = LibraryTrack.ATTRIBUTE_LANGUAGE_LABEL


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
        titleFilter = self.request.query_params.get(FILTER_TITLE_PARAMETER_NAME)
        artistNameFilter = self.request.query_params.get(FILTER_ARTIST_NAME_PARAMETER_NAME)
        albumNameFilter = self.request.query_params.get(FILTER_ALBUM_NAME_PARAMETER_NAME)
        genreNameFilter = self.request.query_params.get(FILTER_GENRE_NAME_PARAMETER_NAME)
        languageFilter = self.request.query_params.get(FILTER_LANGUAGE_PARAMETER_NAME)
        
        if titleFilter is not None:
            queryset = queryset.filter(title__icontains=titleFilter)
        if artistNameFilter is not None:
            queryset = queryset.filter(artist__name__icontains=artistNameFilter)
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
            Updates a track.\n"
            - To not update a field, it mustn't be specified (e.g the line \"artistName\":... 
            shouldn't exist). The only exception is the field 'albumArtistsName' (more 
            precisions below).\n
            - To empty a field (artist or album), the field should be specified with an empty 
            string.\n
            - If the album or the artist is updated, the old artist/album is checked to lookup 
            if it is still linked to something: \n
               - for an album, if no track is linked, it is deleted;\n
               - for an artist, if no track and no album is linked, it is deleted. An artist 
            can have no track linked to it if only it is still linked to an album of a track 
            still in the library. E.g: a user only have one track in his library: 'Jamming' by
            Bob Marley and The Wailers'. The album artists are 'Bob Marley' and 'The Wailers'. 
            The artist 'Bob Marley' is still in the library even if it has no track which has 
            the artist 'Bob Marley'.\n\n" +
            - As two albums can share the same name (e.g from two different artists), the mean 
            the system to identify an album is the peer (album'sname/album's artists'names). 
            Thus:\n" +
               - If it already exists an album with the same name as 'albumName' but with 
            different 'albumArtistsName', an new album is created.\n
               - Wether the field 'albumArtistsName' is empty or not specified, it tells that 
            the track's album has no artist.\n
               - If 'albumName' is empty or missing, the 'albumArtistsName' is ignored.
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
                - some media players allow to edit the rating of a track. In some cases, the
                rating isn't store in the file's metadata but in a seperate database. In those
                cases, the rating won't be imported into Bodzify and will be set to null (= no 
                rating). It is the case for:
                    - iTunes;
                    - Windows Media Player's wav files rating;
                    - Winamp's wav files rating;
            """)
    )
    def create(self, request, *args, **kwargs):
        serializer = TrackPostSchemaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        track = TrackService.Save(
                user=request.user, 
                saveSchemaData=request.data)
        responseSerializer = TrackDetailedSerializer(track)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
                data=TrackDetailedSerializer(track).data,
                status=status.HTTP_200_OK,
                headers=headers)


    @extend_schema(
        parameters=[
            OpenApiParameter(
                    name=LibraryTrack.ATTRIBUTE_TITLE_LABEL, 
                    type=OpenApiTypes.STR, 
                    location=OpenApiParameter.QUERY),
            OpenApiParameter(
                    name=TrackUpdateSchemaSerializer.ATTRIBUTE_ARTIST_NAME_LABEL, 
                    type=OpenApiTypes.STR, 
                    location=OpenApiParameter.QUERY),
            OpenApiParameter(
                    name=TrackUpdateSchemaSerializer.ATTRIBUTE_ALBUM_ARTISTS_NAMES_LABEL, 
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY),
            OpenApiParameter(
                    name=TrackUpdateSchemaSerializer.ATTRIBUTE_GENRE_NAME_LABEL, 
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
