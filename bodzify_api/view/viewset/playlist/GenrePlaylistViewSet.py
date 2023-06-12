#!/usr/bin/env python
from bodzify_api.model.playlist.criteria.GenrePlaylist import GenrePlaylist
from bodzify_api.serializer.playlist.output.GenrePlaylistWithTrackSerializer import \
    GenrePlaylistWithTracksSerializer
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.criteria.CriteriaPlaylist import \
    ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL


class GenrePlaylistViewSet(MultiSerializerViewSet):
    queryset = GenrePlaylist.objects.all()
    serializers = {
        'default': GenrePlaylistWithTracksSerializer,
        'list':  GenrePlaylistWithTracksSerializer,
        'retrieve':  GenrePlaylistWithTracksSerializer,
    }

    def get_queryset(self):
        queryset = GenrePlaylist.objects.filter(user=self.request.user)

        name = self.request.query_params.get(PLAYLIST_ATTRIBUTES_LABEL.NAME)
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
