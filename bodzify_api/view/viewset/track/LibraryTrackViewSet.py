#!/usr/bin/env python

import os

from rest_framework.decorators import action
from rest_framework import status

from drf_spectacular.utils import extend_schema

from django.http import JsonResponse
from django.http import HttpResponse

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
        genre = self.request.query_params.get(GENRE_PARAMETER)
        if genre is not None:
            queryset = queryset.filter(genre=genre)
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
        if os.path.exists(track.file.path):
            return utility.GetFileResponse(filePath=track.file.path, filename=track.file.name)
        else:
            track.delete()
            return HttpResponse(
                content="""The requested track doesn't exist anymore. It is therefore deleted.""",
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
