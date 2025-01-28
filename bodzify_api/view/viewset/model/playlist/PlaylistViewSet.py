from django.core.exceptions import ImproperlyConfigured
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema  # type: ignore
from rest_framework.request import Request

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Fields import Fields
from bodzify_api.model.playlist.PlaylistTypesLabel import PlaylistTypesLabel
from bodzify_api.model.playlist.children.criteria.CriterialessPlaylistNames import CriterialessPlaylistNames
from bodzify_api.serializer.schema.model.playlist.base.output.detailed import PlaylistDetailedSerializer
from bodzify_api.serializer.schema.model.playlist.base.output.simple import PlaylistSimpleSerializer
from bodzify_api.view.viewset.model.base.AppModelViewSet import AppModelViewSet
from bodzify_api.filtering.set.playlist.PlaylistFilterSet import PlaylistFilterSet
from bodzify_api.filtering.set.playlist.Fields import Fields as QueryParamsFields


class PlaylistViewSet(AppModelViewSet[Playlist]):

    def __init__(self, **kwargs):
        super().__init__(model_class=Playlist,
                         filterset_class=PlaylistFilterSet,
                         simple_serializer_class=PlaylistSimpleSerializer,
                         detailed_serializer_class=PlaylistDetailedSerializer,
                         **kwargs)

    @staticmethod
    def _get_queryset_str_filter_value_to_filter_nothing():
        return ''

    def get_queryset(self):
        if self.action == 'retrieve':
            return Playlist.objects.filter(user=self.request.user, uuid=self.kwargs[self.lookup_field])

        request: Request = self.request  # type: ignore
        if not self.filterset_class:
            raise ImproperlyConfigured('Filter class is not defined')

        self.filterset = self.filterset_class(data=request.query_params, queryset=self.queryset)
        query_params_validated = request.query_params

        name_query_param = query_params_validated.get(QueryParamsFields.NAME,
                                                      self._get_queryset_str_filter_value_to_filter_nothing())
        type_query_param = query_params_validated.get(QueryParamsFields.TYPE_LABEL)

        queryset = Playlist.objects.filter(user=self.request.user)

        manual_playlist_queryset = Playlist.objects.none()
        if type_query_param is None or type_query_param.lower() == PlaylistTypesLabel.MANUAL.lower():
            manual_playlist_queryset = queryset.filter(manual_playlist__isnull=False,
                                                       manual_playlist__name__icontains=name_query_param)

        criteria_playlist_queryset = Playlist.objects.none()
        if type_query_param is None or type_query_param.lower() in [PlaylistTypesLabel.GENRE.lower(),
                                                                    PlaylistTypesLabel.TAG.lower()]:
            criteria_playlist_queryset = queryset.filter(
                criteria_playlist__isnull=False,
                criteria_playlist__type__label__icontains=type_query_param.upper()
                if type_query_param else '', criteria_playlist__criteria__name__icontains=name_query_param)

        genreless_playlist = Playlist.objects.none()
        if (not name_query_param or name_query_param.lower() in CriterialessPlaylistNames.GENRE.lower()) \
                and type_query_param in [None, PlaylistTypesLabel.GENRE]:
            genreless_playlist = queryset.filter(criteria_playlist__isnull=False,
                                                 criteria_playlist__criteria__isnull=True,
                                                 criteria_playlist__type_id=CriteriaTypePks.GENRE)

        tagless_playlist = Playlist.objects.none()
        if (not name_query_param or name_query_param.lower() in CriterialessPlaylistNames.TAG.lower()) \
                and type_query_param in [None, PlaylistTypesLabel.TAG]:
            tagless_playlist = queryset.filter(criteria_playlist__isnull=False,
                                               criteria_playlist__criteria__isnull=True,
                                               criteria_playlist__type_id=CriteriaTypePks.TAG)

        return manual_playlist_queryset.union(criteria_playlist_queryset).union(genreless_playlist).union(
            tagless_playlist).order_by(Fields.CREATED_ON)

    @extend_schema(parameters=[OpenApiParameter(name=QueryParamsFields.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=QueryParamsFields.TYPE_LABEL,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, *args, **kwargs):
        return self._handle_list()

    def retrieve(self, *args, **kwargs):
        return self._handle_retrieve()
