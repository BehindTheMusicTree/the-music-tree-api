#!/usr/bin/env python

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes  # type: ignore
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.children.SimplePlaylist import TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL
from bodzify_api.model.playlist.children.CriteriaPlaylist \
    import TypesLabel as CriteriaPlaylistTypesLabels, SpecialNames as CriteriaPlaylistSpecialNames
from bodzify_api.serializer.playlist.base.input.query_param \
    import BasePlaylistQueryParamSerializer, Fields as QueryParams
from bodzify_api.service.Service import Service
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist, AttributesLabel
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet
from bodzify_api.serializer.playlist.base.output.with_tracks import BasePlaylistWithTracksSerializer


class PlaylistViewSet(AppModelViewSet):
    queryset = BasePlaylist.objects.all()
    serializers = {
        'default': BasePlaylistWithTracksSerializer,
        'list':  BasePlaylistWithTracksSerializer,
        'retrieve':  BasePlaylistWithTracksSerializer,
    }

    @staticmethod
    def _get_queryset_str_filter_value_to_filter_nothing():
        return ''

    def __init__(self, **kwargs):
        super().__init__(service=Service(), **kwargs)

    def _get_detailed_serializer(self, instance):
        return BasePlaylistWithTracksSerializer(instance=instance)

    def get_queryset(self):
        if self.action == 'retrieve':
            return BasePlaylist.objects.filter(user=self.request.user, uuid=self.kwargs[self.lookup_field])

        serializer = BasePlaylistQueryParamSerializer(data=self.request.query_params)  # type: ignore
        serializer.is_valid(raise_exception=True)
        query_params_validated = serializer.validated_data

        queryset = BasePlaylist.objects.filter(user=self.request.user)

        if QueryParams.NAME in query_params_validated:  # type: ignore
            name_query_param = query_params_validated.get(QueryParams.NAME)  # type: ignore
        else:
            name_query_param = self._get_queryset_str_filter_value_to_filter_nothing()

        if QueryParams.TYPE in query_params_validated:  # type: ignore
            type_query_param = query_params_validated.get(QueryParams.TYPE)  # type: ignore
        else:
            type_query_param = None

        simple_playlist_queryset = BasePlaylist.objects.none()
        if type_query_param is None or type_query_param.lower() == SIMPLE_PLAYLIST_TYPE_LABEL.lower():
            simple_playlist_queryset = queryset.filter(
                simple_playlist__isnull=False,
                simple_playlist__name__icontains=name_query_param)

        criteria_playlist_queryset = BasePlaylist.objects.none()
        if type_query_param is None or type_query_param.lower() in [CriteriaPlaylistTypesLabels.GENRE.lower(),
                                                                    CriteriaPlaylistTypesLabels.TAG.lower()]:
            criteria_playlist_queryset = queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__type__label__icontains=type_query_param.upper()
                if type_query_param is not None else '',
                criteria_playlist__criteria__name__icontains=name_query_param)

        genreless_playlist = BasePlaylist.objects.none()
        if name_query_param.lower() in CriteriaPlaylistSpecialNames.GENRELESS.lower() \
                and type_query_param in [None, CriteriaPlaylistTypesLabels.GENRE]:  # type: ignore
            genreless_playlist = queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__criteria__isnull=True,
                criteria_playlist__type_id=CriteriaTypesId.GENRE)

        tagless_playlist = BasePlaylist.objects.none()
        if name_query_param.lower() in CriteriaPlaylistSpecialNames.TAGLESS.lower() \
                and type_query_param in [None, CriteriaPlaylistTypesLabels.TAG]:
            tagless_playlist = queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__criteria__isnull=True,
                criteria_playlist__type_id=CriteriaTypesId.TAG)

        return simple_playlist_queryset.union(criteria_playlist_queryset).union(genreless_playlist).union(
            tagless_playlist).order_by(AttributesLabel.CREATED_ON)

    @extend_schema(parameters=[OpenApiParameter(name=QueryParams.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=QueryParams.TYPE,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super()._list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
