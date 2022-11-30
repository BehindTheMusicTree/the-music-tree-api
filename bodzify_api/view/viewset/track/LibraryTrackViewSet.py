#!/usr/bin/env python

from rest_framework.decorators import action
from rest_framework import status

from drf_spectacular.utils import extend_schema

from django.http import JsonResponse

from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackSerializer
from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackResponseSerializer
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.service import LibraryTrackService
from bodzify_api.view import utility

GENRE_PARAM = "genre"

class LibraryTrackViewSet(MultiSerializerViewSet):
    queryset = LibraryTrack.objects.all()
    serializers = {
        'default': LibraryTrackSerializer,
        'list':  LibraryTrackResponseSerializer,
        'retrieve':  LibraryTrackResponseSerializer,
    }

    def get_queryset(self):
        queryset = LibraryTrack.objects.filter(user=self.request.user)
        genre = self.request.query_params.get(GENRE_PARAM)
        if genre is not None: queryset = queryset.filter(genre=genre)
        return queryset

    @extend_schema(
        request=LibraryTrackSerializer,
        responses=LibraryTrackResponseSerializer
    )
    def update(self, request, *args, **kwargs):
        updatedTrack = LibraryTrackService.update(
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
        return utility.GetFileResponseForTrackDownload(
            request=request, 
            track=LibraryTrack.objects.get(uuid=pk))
        