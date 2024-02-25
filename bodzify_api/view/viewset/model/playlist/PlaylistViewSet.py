#!/usr/bin/env python

from django.http import JsonResponse
from rest_framework import status
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist, TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist, \
    TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.playlist.output.PlaylistGetParamSerializer import \
    ATTRIBUTES_LABEL as PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithTracksSerializer import \
    CriteriaPlaylistWithTracksSerializer
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import LibTrackDetailedSerializer
from bodzify_api.service.playlist.PlaylistService import PlaylistService
from bodzify_api.view.pagination.DefaultMultipleModelLimitOffsetPagination import \
    DefaultMultipleModelLimitOffsetPagination
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import \
    ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL


class PlaylistViewSet(ObjectMultipleModelAPIViewSet):

    pagination_class = DefaultMultipleModelLimitOffsetPagination
    serializers = {
        'default': CriteriaPlaylistWithTracksSerializer,
        'list':  CriteriaPlaylistWithTracksSerializer,
        'retrieve':  CriteriaPlaylistWithTracksSerializer,
    }

    def get_queryset(self):
        type_key = PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL.TYPE
        if type_key in self.request.GET:
            type_filter = self.request.GET[type_key]
            if type_filter == SIMPLE_PLAYLIST_TYPE_LABEL:
                queryset = SimplePlaylist.objects.filter(
                    playlist__user=self.request.user)
            elif type_filter == CRITERIA_PLAYLIST_TYPES_LABEL.GENRE:
                queryset = CriteriaPlaylist.objects.filter(
                    playlist__user=self.request.user, type_id=CRITERIA_TYPES_ID.GENRE)
            elif type_filter == CRITERIA_PLAYLIST_TYPES_LABEL.TAG:
                queryset = CriteriaPlaylist.objects.filter(
                    playlist__user=self.request.user, type_id=CRITERIA_TYPES_ID.TAG)
        else:
            queryset = CriteriaPlaylist.objects.filter(user=self.request.user)

            parent_uuid_param_key = CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT
            if parent_uuid_param_key not in self.request.GET:
                queryset = queryset | SimplePlaylist.objects.filter(playlist__user=self.request.user)
            else:
                queryset = queryset.filter(
                    parent__uuid=self.request.GET[parent_uuid_param_key])

        name_key = ATTRIBUTES_LABEL.NAME
        if name_key in self.request.GET:
            queryset = queryset.filter(
                name__icontains=self.request.GET[name_key])

        return queryset

    @extend_schema(parameters=[OpenApiParameter(name=ATTRIBUTES_LABEL.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL.TYPE,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
