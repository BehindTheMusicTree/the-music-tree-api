#!/usr/bin/env python

import logging
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # type: ignore
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.children.SimplePlaylist import TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL
from bodzify_api.model.playlist.children.CriteriaPlaylist \
    import TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL, SPECIAL_NAMES as CRITERIA_PLAYLIST_SPECIAL_NAMES
from bodzify_api.serializer.playlist.mother.input.PlaylistQueryParamSerializer \
    import PlaylistQueryParamSerializer, FIELDS as QUERY_PARAM_FIELDS
from bodzify_api.service.Service import Service
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.serializer.playlist.mother.output.PlaylistWithTracksSerializer import PlaylistWithTracksSerializer

logger = logging.getLogger('bodyzify_api')


class PlaylistViewSet(AppModelViewSet):
    queryset = Playlist.objects.all()
    serializers = {
        'default': PlaylistWithTracksSerializer,
        'list':  PlaylistWithTracksSerializer,
        'retrieve':  PlaylistWithTracksSerializer,
    }

    @staticmethod
    def _get_queryset_str_filter_value_to_filter_nothing():
        return ''

    def __init__(self, **kwargs):
        super().__init__(service=Service(), **kwargs)

    def _get_detailed_serializer(self, instance):
        return PlaylistWithTracksSerializer(instance=instance)

    def get_queryset(self):
        if self.action == 'retrieve':
            return Playlist.objects.filter(user=self.request.user, uuid=self.kwargs[self.lookup_field])

        serializer = PlaylistQueryParamSerializer(data=self.request.query_params)  # type: ignore
        serializer.is_valid(raise_exception=True)
        query_params_validated = serializer.validated_data

        queryset = Playlist.objects.filter(user=self.request.user)

        if QUERY_PARAM_FIELDS.NAME in query_params_validated:  # type: ignore
            name_query_param = query_params_validated.get(QUERY_PARAM_FIELDS.NAME)  # type: ignore
        else:
            name_query_param = self._get_queryset_str_filter_value_to_filter_nothing()

        if QUERY_PARAM_FIELDS.TYPE in query_params_validated:  # type: ignore
            type_query_param = query_params_validated.get(QUERY_PARAM_FIELDS.TYPE)  # type: ignore
        else:
            type_query_param = None

        simple_playlist_queryset = Playlist.objects.none()
        if type_query_param is None or type_query_param.lower() == SIMPLE_PLAYLIST_TYPE_LABEL.lower():
            simple_playlist_queryset = queryset.filter(
                simple_playlist__isnull=False,
                simple_playlist__name__icontains=name_query_param)

        criteria_playlist_queryset = Playlist.objects.none()
        if type_query_param is None or type_query_param.lower() in [CRITERIA_PLAYLIST_TYPES_LABEL.GENRE.lower(),
                                                                    CRITERIA_PLAYLIST_TYPES_LABEL.TAG.lower()]:
            criteria_playlist_queryset = queryset.filter(
                criteria_playlist__isnull=False, criteria_playlist__type__label__icontains=type_query_param.upper()
                if type_query_param is not None else '', criteria_playlist__criteria__name__icontains=name_query_param)

        genreless_playlist = Playlist.objects.none()
        if name_query_param.lower() in CRITERIA_PLAYLIST_SPECIAL_NAMES.GENRELESS.lower() \
                and type_query_param in [None, CRITERIA_PLAYLIST_TYPES_LABEL.GENRE]:  # type: ignore
            genreless_playlist = queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__criteria__isnull=True,
                criteria_playlist__type_id=CRITERIA_TYPES_ID.GENRE)

        tagless_playlist = Playlist.objects.none()
        if name_query_param.lower() in CRITERIA_PLAYLIST_SPECIAL_NAMES.TAGLESS.lower() \
                and type_query_param in [None, CRITERIA_PLAYLIST_TYPES_LABEL.TAG]:  # type: ignore
            tagless_playlist = queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__criteria__isnull=True,
                criteria_playlist__type_id=CRITERIA_TYPES_ID.TAG)

        return simple_playlist_queryset.union(
            criteria_playlist_queryset).union(genreless_playlist).union(tagless_playlist)

    @extend_schema(parameters=[OpenApiParameter(name=QUERY_PARAM_FIELDS.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=QUERY_PARAM_FIELDS.TYPE,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super()._list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
