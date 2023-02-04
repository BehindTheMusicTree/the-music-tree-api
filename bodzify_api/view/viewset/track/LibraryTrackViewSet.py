#!/usr/bin/env python

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

TITLE_PARAMETER_NAME = "title"
ARTIST_PARAMETER_NAME = "artist"
ALBUM_PARAMETER_NAME = "album"
GENRE_PARAMETER_NAME = "genre"
FILE_PARAMETER_NAME = "file"


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
        title = self.request.query_params.get(TITLE_PARAMETER_NAME)
        artist = self.request.query_params.get(ARTIST_PARAMETER_NAME)
        album = self.request.query_params.get(ALBUM_PARAMETER_NAME)
        genre = self.request.query_params.get(GENRE_PARAMETER_NAME)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if artist is not None:
            queryset = queryset.filter(artist__name__icontains=artist)
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
            user=request.user
        )

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
                content="The requested track's file is missing.",
                status=status.HTTP_410_GONE)


    def create(self, request, *args, **kwargs):
        form = UploadTrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = LibraryTrackService.CreateFromUpload(
                request.user, request.FILES[FILE_PARAMETER_NAME])
            return JsonResponse(
                data=LibraryTrackResponseSerializer(track).data,
                status=status.HTTP_201_CREATED)
        return utility.GetJsonResponseWhenBadRequest(form.errors)


    @extend_schema(
        parameters=[
          OpenApiParameter(
            name=TITLE_PARAMETER_NAME, 
            type=OpenApiTypes.STR, 
            location=OpenApiParameter.QUERY),
          OpenApiParameter(
            name=ARTIST_PARAMETER_NAME, 
            type=OpenApiTypes.STR, 
            location=OpenApiParameter.QUERY),
          OpenApiParameter(
            name=ALBUM_PARAMETER_NAME, 
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY),
          OpenApiParameter(
            name=GENRE_PARAMETER_NAME, 
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
