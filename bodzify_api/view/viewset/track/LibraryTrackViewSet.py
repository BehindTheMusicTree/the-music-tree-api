#!/usr/bin/env python

from django.http import JsonResponse
from django.http import HttpResponse

from rest_framework.decorators import action
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from bodzify_api.serializer.track.TrackDetailedSerializer import (
        TrackDetailedSerializer)
from bodzify_api.serializer.track.TrackPutSerializer import (
        TrackPutSerializer)
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.form.TrackPostForm import TrackPostForm
import bodzify_api.service.LibraryTrackService as LibraryTrackService
import bodzify_api.view.utility as utility

DATA_TITLE_PARAMETER_NAME = "title"
DATA_ARTIST_PARAMETER_NAME = "artist"
DATA_ARTIST_NAME_PARAMETER_NAME = "artistName"
DATA_ALBUM_PARAMETER_NAME = "album"
DATA_ALBUM_NAME_PARAMETER_NAME = "albumName"
DATA_ALBUM_ARTISTS_NAMES_PARAMETER_NAME = "albumArtistsNames"
DATA_GENRE_PARAMETER_NAME = "genre"
DATA_LANGUAGE_PARAMETER_NAME = "language"
DATA_FILE_PARAMETER_NAME = "file"

FILTER_TITLE_PARAMETER_NAME = DATA_TITLE_PARAMETER_NAME
FILTER_ARTIST_NAME_PARAMETER_NAME = DATA_ARTIST_NAME_PARAMETER_NAME
FILTER_ALBUM_NAME_PARAMETER_NAME = DATA_ALBUM_NAME_PARAMETER_NAME
FILTER_ALBUM_ARTISTS_NAME_PARAMETER_NAME = DATA_ALBUM_ARTISTS_NAMES_PARAMETER_NAME
FILTER_GENRE_NAME_PARAMETER_NAME = "genreName"
FILTER_LANGUAGE_PARAMETER_NAME = DATA_LANGUAGE_PARAMETER_NAME


class LibraryTrackViewSet(MultiSerializerViewSet):

    queryset = LibraryTrack.objects.all()
    serializers = {
        'default': TrackDetailedSerializer,
        'list':  TrackDetailedSerializer,
        'retrieve':  TrackDetailedSerializer,
        'update':  TrackPutSerializer,
    }

    def get_queryset(self):
        queryset = LibraryTrack.objects.filter(user=self.request.user)
        title = self.request.query_params.get(FILTER_TITLE_PARAMETER_NAME)
        artistName = self.request.query_params.get(FILTER_ARTIST_NAME_PARAMETER_NAME)
        albumName = self.request.query_params.get(FILTER_ALBUM_NAME_PARAMETER_NAME)
        genreName = self.request.query_params.get(FILTER_GENRE_NAME_PARAMETER_NAME)
        language = self.request.query_params.get(FILTER_LANGUAGE_PARAMETER_NAME)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if artistName is not None:
            queryset = queryset.filter(artist__name__icontains=artistName)
        if albumName is not None:
            queryset = queryset.filter(album__name__icontains=albumName)
        if genreName is not None:
            queryset = queryset.filter(genre__name__icontain=genreName)
        if language is not None:
            queryset = queryset.filter(language__icontains=language)
        return queryset


    @extend_schema(
        request=TrackPutSerializer,
        responses=TrackDetailedSerializer
    )
    def update(self, request, *args, **kwargs):
        updatedTrack = LibraryTrackService.Update(
                oldTrack=self.get_object(),
                newData=request.data,
                partial=kwargs.pop('partial', False),
                TrackPutSerializerClass=TrackPutSerializer,
                user=request.user)
        responseSerializer = TrackDetailedSerializer(updatedTrack)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
                data=TrackDetailedSerializer(updatedTrack).data,
                status=status.HTTP_201_CREATED,
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


    def create(self, request, *args, **kwargs):
        form = TrackPostForm(request.POST, request.FILES)
        if form.is_valid():
            track = LibraryTrackService.CreateFromUpload(
                    request.user, request.FILES[DATA_FILE_PARAMETER_NAME])
            return JsonResponse(
                    data=TrackDetailedSerializer(track).data,
                    status=status.HTTP_201_CREATED)
        return utility.GetJsonResponseWhenBadRequest(form.errors)


    @extend_schema(
        parameters=[
            OpenApiParameter(
                    name=DATA_TITLE_PARAMETER_NAME, 
                    type=OpenApiTypes.STR, 
                    location=OpenApiParameter.QUERY),
            OpenApiParameter(
                    name=DATA_ARTIST_NAME_PARAMETER_NAME, 
                    type=OpenApiTypes.STR, 
                    location=OpenApiParameter.QUERY),
            OpenApiParameter(
                    name=DATA_ALBUM_NAME_PARAMETER_NAME, 
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY),
            OpenApiParameter(
                    name=DATA_GENRE_PARAMETER_NAME, 
                    type=OpenApiTypes.STR,
                    location=OpenApiParameter.QUERY)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
