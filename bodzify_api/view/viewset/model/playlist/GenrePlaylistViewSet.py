#!/usr/bin/env python

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from bodzify_api.model.criteria.Criteria import AttributesLabels as CriteriaAttributesLabels
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist, AttributesLabels
from bodzify_api.serializer.playlist.children.criteria.input.query_param \
    import Fields as QueryParams, CriteriaPlaylistQueryParamSerializer
from bodzify_api.serializer.playlist.children.criteria.output.with_tracks \
    import CriteriaPlaylistWithTracksSerializer
from bodzify_api.serializer.playlist.children.criteria.output.without_tracks \
    import CriteriaPlaylistWithoutTracksSerializer
from bodzify_api.view.viewset.model.AppModelViewSet import AppModelViewSet


class GenrePlaylistViewSet(AppModelViewSet):
    queryset = CriteriaPlaylist.objects.filter(type_id=CriteriaTypesId.GENRE)
    serializers = {
        'default': CriteriaPlaylistWithTracksSerializer,
        'list':  CriteriaPlaylistWithoutTracksSerializer,
        'retrieve':  CriteriaPlaylistWithTracksSerializer,
    }

    def __init__(self, **kwargs):
        super().__init__(None, **kwargs)

    def get_queryset(self):
        serializer = CriteriaPlaylistQueryParamSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        validated_query_params = serializer.validated_data

        queryset = CriteriaPlaylist.objects.filter(
            base_playlist__user=self.request.user, type_id=CriteriaTypesId.GENRE)

        name_query_param = validated_query_params.get(QueryParams.NAME)  # type: ignore
        if name_query_param is not None:
            queryset = queryset.filter(criteria__name__icontains=name_query_param)

        parent_uuid_query_param = validated_query_params.get(QueryParams.PARENT)  # type: ignore
        if parent_uuid_query_param is not None:
            if parent_uuid_query_param == "":
                parent_uuid_query_param = None
            else:
                parent_uuid_query_param = parent_uuid_query_param
            queryset = queryset.filter(base_playlist__user=self.request.user,
                                       criteria__parent__uuid=parent_uuid_query_param)

        return queryset.order_by(f"{AttributesLabels.CRITERIA}__{CriteriaAttributesLabels.NAME}")

    @extend_schema(parameters=[OpenApiParameter(name=QueryParams.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=QueryParams.PARENT,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
