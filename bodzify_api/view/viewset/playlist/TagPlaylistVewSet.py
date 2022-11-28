#!/usr/bin/env python

from rest_framework.decorators import action

from bodzify_api.serializer.playlist.TagPlaylistSerializer import TagPlaylistSerializer
from bodzify_api.model.playlist.TagPlaylist import TagPlaylist
from bodzify_api.model.playlist.PlaylistType import PlaylistTypeLabels
from bodzify_api.view.viewset.playlist.PlaylistViewSet import PlaylistViewSet

PARENT_PARAMETER = "parent"

class TagPlaylistViewSet(PlaylistViewSet):  
    serializers = {
        'default': TagPlaylistSerializer,
        'list':  TagPlaylistSerializer,
        'retrieve':  TagPlaylistSerializer,
    }

    def __init__(self, playlistTypeLabel=PlaylistTypeLabels.TAG, **kwargs): 
        super(TagPlaylistViewSet, self).__init__(playlistTypeLabel, **kwargs)

    def get_queryset(self):
        queryset = TagPlaylist.objects.filt
        
        parent = self.request.query_params.get(PARENT_PARAMETER)
        if parent is not None: queryset = queryset.filter(genre__parent__name=parent)

        return queryset