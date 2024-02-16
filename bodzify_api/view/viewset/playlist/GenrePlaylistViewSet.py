#!/usr/bin/env python
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.playlist.criteria.genre.output.GenrePlaylistWithTracksSerializer import \
    CriteriaPlaylistWithTracksSerializer
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import \
    ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL


class GenrePlaylistViewSet(MultiSerializerViewSet):
    queryset = CriteriaPlaylist.objects.filter(type_id=CRITERIA_TYPES_ID.GENRE)
    serializers = {
        'default': CriteriaPlaylistWithTracksSerializer,
        'list':  CriteriaPlaylistWithTracksSerializer,
        'retrieve':  CriteriaPlaylistWithTracksSerializer,
    }

    def get_queryset(self):
        queryset = CriteriaPlaylist.objects.filter(
            user=self.request.user, type_id=CRITERIA_TYPES_ID.GENRE)

        name = self.request.query_params.get(ATTRIBUTES_LABEL.NAME)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        parentUuidParameterValue = self.request.query_params.get(
            CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT)
        if parentUuidParameterValue is not None:
            if parentUuidParameterValue == "":
                parentUuidFilter = None
            else:
                parentUuidFilter = parentUuidParameterValue
            queryset = queryset.filter(criteria__parent__uuid=parentUuidFilter)

        return queryset
