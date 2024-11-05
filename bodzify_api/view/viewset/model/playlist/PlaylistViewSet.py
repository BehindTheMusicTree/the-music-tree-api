from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema  # type: ignore
from rest_framework.request import Request
from django.contrib.contenttypes.models import ContentType

from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.Fields import Fields
from bodzify_api.model.playlist.children.ChildPlaylistTypes import ChildPlaylistTypes
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylistWithoutCriteriaNames \
    import CriteriaPlaylistWithoutCriteriaNames
from bodzify_api.model.playlist.children.criteria.children.genre.GenrePlaylist import GenrePlaylist
from bodzify_api.serializer.schema.playlist.base.output.simple import BasePlaylistSimpleSerializer
from bodzify_api.view.viewset.base.AppModelViewSet import AppModelViewSet
from bodzify_api.filter.set.playlist.PlaylistParamFilterSet import PlaylistParamFilterSet
from bodzify_api.filter.set.playlist.Fields import Fields as QueryParamsFields


class PlaylistViewSet(AppModelViewSet[BasePlaylist]):

    def __init__(self, **kwargs):
        super().__init__(model_class=BasePlaylist,
                         filter_class=PlaylistParamFilterSet,
                         simple_serializer_class=BasePlaylistSimpleSerializer,
                         **kwargs)

    @staticmethod
    def _get_queryset_str_filter_value_to_filter_nothing():
        return ''

    def get_queryset(self):
        if self.action == 'retrieve':
            return BasePlaylist.objects.filter(user=self.request.user, uuid=self.kwargs[self.lookup_field])

        request: Request = self.request  # type: ignore
        if not self.filter_class:
            raise Exception('Filter class is not defined')
        self.filterset = self.filter_class(data=request.query_params, queryset=self.queryset)
        query_params_validated = request.query_params

        name_query_param = query_params_validated.get(QueryParamsFields.NAME,
                                                      self._get_queryset_str_filter_value_to_filter_nothing())
        type_query_param = query_params_validated.get(QueryParamsFields.TYPE)

        queryset = BasePlaylist.objects.filter(user=self.request.user)

        manual_playlist_queryset = BasePlaylist.objects.none()
        if type_query_param is None or type_query_param.lower() == ChildPlaylistTypes.MANUAL.lower():
            manual_playlist_queryset = queryset.filter(simple_child_playlist__isnull=False,
                                                       simple_child_playlist__name__icontains=name_query_param)

        criteria_playlist_queryset = BasePlaylist.objects.none()
        if type_query_param is None or type_query_param.lower() in [ChildPlaylistTypes.GENRE.lower(),
                                                                    ChildPlaylistTypes.TAG.lower()]:
            criteria_playlist_queryset = queryset.filter(
                criteria_child_playlist__isnull=False,
                criteria_child_playlist__type__label__icontains=type_query_param.upper()
                if type_query_param else '',
                criteria_child_playlist__criteria__name__icontains=name_query_param)

        genreless_playlist = BasePlaylist.objects.none()
        if (not name_query_param or name_query_param.lower() in CriteriaPlaylistWithoutCriteriaNames.GENRE.lower()) \
                and type_query_param in [None, ChildPlaylistTypes.GENRE]:
            genreless_playlist = queryset.filter(
                criteria_child_playlist__isnull=False,
                criteria_child_playlist__criteria__isnull=True,
                criteria_child_playlist__type_id=ChildPlaylistTypes.GENRE)

        tagless_playlist = BasePlaylist.objects.none()
        if (not name_query_param or name_query_param.lower() in CriteriaPlaylistWithoutCriteriaNames.TAG.lower()) \
                and type_query_param in [None, ChildPlaylistTypes.TAG]:
            tagless_playlist = queryset.filter(
                criteria_child_playlist__isnull=False,
                criteria_child_playlist__criteria__isnull=True,
                criteria_child_playlist__type_id=CriteriaTypesId.TAG)

        return manual_playlist_queryset.union(criteria_playlist_queryset).union(genreless_playlist).union(
            tagless_playlist).order_by(Fields.CREATED_ON)

    @extend_schema(parameters=[OpenApiParameter(name=QueryParamsFields.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=QueryParamsFields.TYPE,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super()._handle_list(request, *args, **kwargs)
