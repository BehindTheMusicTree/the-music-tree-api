#!/usr/bin/env python

from django.http import JsonResponse
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.criteria.GenrePlaylist import GenrePlaylist
from bodzify_api.model.playlist.criteria.TagPlaylist import TagPlaylist
from bodzify_api.serializer.playlist.PlaylistGetParamSerializer import \
    ATTRIBUTES_LABEL as PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.PlaylistWithTrackSerializer import PlaylistWithTracksSerializer
from bodzify_api.service.PlaylistService import PlaylistService
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.criteria.CriteriaPlaylist import \
    ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL


class PlaylistViewSet(MultiSerializerViewSet):
    serializers = {
        'default': PlaylistWithTracksSerializer,
        'list':  PlaylistWithTracksSerializer,
        'retrieve':  PlaylistWithTracksSerializer,
    }

    def get_queryset(self):
        typekey = PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL.TYPE
        if typekey in self.request.GET:
            typeFilter = self.request.GET[typekey]
            if typeFilter == SimplePlaylist.TYPE_LABEL:
                queryset = SimplePlaylist.objects.filter(
                    user=self.request.user)
            elif typeFilter == GenrePlaylist.TYPE_LABEL:
                queryset = GenrePlaylist.objects.filter(user=self.request.user)
            elif typeFilter == TagPlaylist.TYPE_LABEL:
                queryset = TagPlaylist.objects.filter(user=self.request.user)
        else:
            queryset = GenrePlaylist.objects.filter(user=self.request.user) | \
                TagPlaylist.objects.filter(user=self.request.user)

            parentUuidParamKey = CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT
            if parentUuidParamKey not in self.request.GET:
                queryset = queryset | SimplePlaylist.objects.filter(
                    user=self.request.user)
            else:
                queryset = queryset.filter(
                    parent__uuid=self.request.GET[parentUuidParamKey])

        nameKey = PLAYLIST_ATTRIBUTES_LABEL.NAME
        if nameKey in self.request.GET:
            queryset = queryset.filter(
                name__icontains=self.request.GET[nameKey])

        return queryset

    @extend_schema(parameters=[OpenApiParameter(name=PLAYLIST_ATTRIBUTES_LABEL.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL.TYPE,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        simplePlaylist = PlaylistService().createSimplePlaylist(
            self.request.user, self.request.data)
        
        responseSerializer = PlaylistWithTracksSerializer(simplePlaylist)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
            data=responseSerializer.data, status=status.HTTP_201_CREATED, headers=headers)
