#!/usr/bin/env python

import os

from django.http import JsonResponse
from django.http import HttpResponse

from rest_framework.decorators import action
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackSerializer
from bodzify_api.serializer.track.LibraryTrackResponseSerializer import (
    LibraryTrackResponseSerializer
)
from bodzify_api.serializer.track.LibraryTrackUpdateRequestSerializer import (
    LibraryTrackUpdateRequestSerializer
)
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.form.UploadTrackForm import UploadTrackForm
import bodzify_api.service.LibraryTrackService as LibraryTrackService
import bodzify_api.view.utility as utility

TITLE_PARAMETER = "title"
ARTIST_PARAMETER = "artist"
ALBUM_PARAMETER = "album"
GENRE_PARAMETER = "genre"
FILE_PARAMETER = "file"


class LibraryTrackViewSet(MultiSerializerViewSet):
    queryset = LibraryTrack.objects.all()
    serializers = {
        'default': LibraryTrackSerializer,
        'list':  LibraryTrackResponseSerializer,
        'retrieve':  LibraryTrackResponseSerializer,
        'update':  LibraryTrackUpdateRequestSerializer,
    }

    def get_queryset(self):
        queryset = LibraryTrack.objects.filter(user=self.request.user)
        title = self.request.query_params.get(TITLE_PARAMETER)
        artist = self.request.query_params.get(ARTIST_PARAMETER)
        album = self.request.query_params.get(ALBUM_PARAMETER)
        genre = self.request.query_params.get(GENRE_PARAMETER)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if artist is not None:
            queryset = queryset.filter(artist__icontains=artist)
        if album is not None:
            queryset = queryset.filter(album__icontains=album)
        if genre is not None:
            queryset = queryset.filter(genre__icontains=genre)
        return queryset

    @extend_schema(
        request=LibraryTrackUpdateRequestSerializer,
        responses=LibraryTrackResponseSerializer
    )
    def update(self, request, *args, **kwargs):
        updatedTrack = LibraryTrackService.Update(
            track=self.get_object(),
            data=request.data,
            partial=kwargs.pop('partial', False),
            RequestSerializerClass=LibraryTrackSerializer,
            user=request.user)

        responseSerializer = LibraryTrackResponseSerializer(updatedTrack)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
            data=responseSerializer.data, status=status.HTTP_200_OK, headers=headers)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        track = LibraryTrack.objects.get(uuid=pk)
        if track.fileExists:
            return utility.GetFileResponse(filePath=track.file.path, filename=track.file.name)
        else:
            return HttpResponse(
                content="The requested track'sfile is missing.",
                status=status.HTTP_410_GONE)

    def create(self, request, *args, **kwargs):
        form = UploadTrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = LibraryTrackService.CreateFromUpload(
                request.user, request.FILES[FILE_PARAMETER])
            return JsonResponse(
                data=LibraryTrackResponseSerializer(track).data,
                status=status.HTTP_201_CREATED)
        return utility.GetJsonResponseWhenBadRequest(form.errors)

    @extend_schema(
        parameters=[
          OpenApiParameter(
            name=TITLE_PARAMETER, 
            type=OpenApiTypes.STR, 
            location=OpenApiParameter.QUERY),
          OpenApiParameter(
            name=ARTIST_PARAMETER, 
            type=OpenApiTypes.STR, 
            location=OpenApiParameter.QUERY),
          OpenApiParameter(
            name=ALBUM_PARAMETER, 
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY),
          OpenApiParameter(
            name=GENRE_PARAMETER, 
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)