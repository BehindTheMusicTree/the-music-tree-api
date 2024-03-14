#!/usr/bin/env python

from venv import logger
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # type: ignore
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.SimplePlaylist import TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL
from bodzify_api.model.playlist.children.CriteriaPlaylist import TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL
from bodzify_api.serializer.playlist.mother.input.PlaylistQueryParamSerializer \
    import PlaylistQueryParamSerializer, FIELDS as QUERY_PARAM_FIELDS
from bodzify_api.service.Service import Service
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.serializer.playlist.mother.output.PlaylistWithTracksSerializer import PlaylistWithTracksSerializer


class PlaylistViewSet(AppModelViewSet):
    queryset = Playlist.objects.all()
    serializers = {
        'default': PlaylistWithTracksSerializer,
        'list':  PlaylistWithTracksSerializer,
        'retrieve':  PlaylistWithTracksSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(service=Service(), **kwargs)

    def _get_detailed_serializer(self, instance):
        return PlaylistWithTracksSerializer(instance=instance)

    def get_queryset(self):
        serializer = PlaylistQueryParamSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        query_params_validated = serializer.validated_data

        type_query_param = query_params_validated.get(QUERY_PARAM_FIELDS.TYPE)  # type: ignore
        if type_query_param is not None:
            if type_query_param == SIMPLE_PLAYLIST_TYPE_LABEL:
                queryset = Playlist.objects.filter(simple_playlist__isnull=False, playlist__user=self.request.user)
            elif type_query_param == CRITERIA_PLAYLIST_TYPES_LABEL.GENRE:
                queryset = Playlist.objects.filter(
                    criteria_playlist__isnull=False,
                    user=self.request.user,
                    criteria_playlist__type_id=CRITERIA_TYPES_ID.GENRE)
            elif type_query_param == CRITERIA_PLAYLIST_TYPES_LABEL.TAG:
                queryset = Playlist.objects.filter(
                    criteria_playlist__isnull=False,
                    user=self.request.user,
                    criteria_playlist__type_id=CRITERIA_TYPES_ID.TAG)
        else:
            queryset = Playlist.objects.filter(user=self.request.user)

        # name_key = PLAYLIST_ATTRIBUTES_LABEL.NAME
        # if name_key in self.request.GET:
        #     queryset = queryset.filter(
        #         name__icontains=self.request.GET[name_key])

        return queryset

    @extend_schema(parameters=[OpenApiParameter(name=QUERY_PARAM_FIELDS.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=QUERY_PARAM_FIELDS.TYPE,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super()._list(request, *args, **kwargs)
