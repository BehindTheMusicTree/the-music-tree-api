#!/usr/bin/env python

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.CriteriaPlaylist \
    import CriteriaPlaylist, ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithTracksSerializer import \
    CriteriaPlaylistWithTracksSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class GET_QUERY_FIELDS:
    NAME = PLAYLIST_ATTRIBUTES_LABEL.NAME
    PARENT = CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT


class GenrePlaylistViewSet(AppModelViewSet):
    queryset = CriteriaPlaylist.objects.filter(type_id=CRITERIA_TYPES_ID.GENRE)
    serializers = {
        'default': CriteriaPlaylistWithTracksSerializer,
        'list':  CriteriaPlaylistWithTracksSerializer,
        'retrieve':  CriteriaPlaylistWithTracksSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(None, **kwargs)

    def get_queryset(self):
        queryset = CriteriaPlaylist.objects.filter(playlist__user=self.request.user, type_id=CRITERIA_TYPES_ID.GENRE)

        name = self.request.query_params.get(GET_QUERY_FIELDS.NAME)  # type: ignore
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        parent_uuid_parameter_value = self.request.query_params.get(GET_QUERY_FIELDS.PARENT)  # type: ignore
        if parent_uuid_parameter_value is not None:
            if parent_uuid_parameter_value == "":
                parent_uuid_filter = None
            else:
                parent_uuid_filter = parent_uuid_parameter_value
            queryset = queryset.filter(criteria__parent__uuid=parent_uuid_filter)

        return queryset

    @extend_schema(parameters=[
        OpenApiParameter(name=GET_QUERY_FIELDS.NAME,
                         type=OpenApiTypes.STR,
                         location=OpenApiParameter.QUERY),
        OpenApiParameter(name=GET_QUERY_FIELDS.PARENT,
                         type=OpenApiTypes.STR,
                         location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
