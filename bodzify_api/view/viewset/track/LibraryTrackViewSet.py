#!/usr/bin/env python

from rest_framework.decorators import action
from rest_framework import status

from drf_spectacular.utils import extend_schema

from django.http import JsonResponse

from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackSerializer
from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackResponseSerializer
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
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
    }


    def get_queryset(self):
        queryset = LibraryTrack.objects.filter(user=self.request.user)
        genre = self.request.query_params.get(GENRE_PARAMETER)
        if genre is not None: queryset = queryset.filter(genre=genre)
        return queryset


    @extend_schema(
        request=LibraryTrackSerializer,
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
        return JsonResponse(responseSerializer.data, status=status.HTTP_201_CREATED, headers=headers)


    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        track = LibraryTrack.objects.get(uuid=pk)
        return utility.GetFileResponse(request=request, filePath=track.path, filename=track.filename)


    def create(self, request, *args, **kwargs):  
        track = LibraryTrackService.CreateFromUpload(request.user, request.FILES[FILE_PARAMETER])
        return JsonResponse(LibraryTrackResponseSerializer(track).data)
