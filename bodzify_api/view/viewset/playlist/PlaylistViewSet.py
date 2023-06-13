#!/usr/bin/env python

from django.http import JsonResponse
from rest_framework import status
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist
from bodzify_api.model.playlist.criteria.GenrePlaylist import GenrePlaylist
from bodzify_api.model.playlist.criteria.TagPlaylist import TagPlaylist
from bodzify_api.serializer.playlist.output.PlaylistGetParamSerializer import \
    ATTRIBUTES_LABEL as PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.output.CriteriaPlaylistWithTrackSerializer import CriteriaPlaylistWithTracksSerializer
from bodzify_api.service.PlaylistService import PlaylistService
from bodzify_api.view.pagination.DefaultMultipleModelLimitOffsetPagination import DefaultMultipleModelLimitOffsetPagination
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.criteria.CriteriaPlaylist import \
    ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL


class PlaylistViewSet(ObjectMultipleModelAPIViewSet):
    pagination_class = DefaultMultipleModelLimitOffsetPagination
    serializers = {
        'default': CriteriaPlaylistWithTracksSerializer,
        'list':  CriteriaPlaylistWithTracksSerializer,
        'retrieve':  CriteriaPlaylistWithTracksSerializer,
    }

    def get_queryset(self):
        typekey = PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL.TYPE
        if typekey in self.request.GET:
            typeFilter = self.request.GET[typekey]
            if typeFilter == SimplePlaylist.TYPE_LABEL:
                queryset = SimplePlaylist.objects.filter(
                    user=self.request.user)
            elif typeFilter == GenrePlaylist.TYPE_LABEL:
                queryset = GenrePlaylist.objects.filter(user=self.request.user)
            elif typeFilter == TagPlaylist.TYPE_LABEL:
                queryset = TagPlaylist.objects.filter(user=self.request.user)
        else:
            queryset = GenrePlaylist.objects.filter(user=self.request.user) | \
                TagPlaylist.objects.filter(user=self.request.user)

            parentUuidParamKey = CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT
            if parentUuidParamKey not in self.request.GET:
                queryset = queryset | SimplePlaylist.objects.filter(
                    user=self.request.user)
            else:
                queryset = queryset.filter(
                    parent__uuid=self.request.GET[parentUuidParamKey])

        nameKey = PLAYLIST_ATTRIBUTES_LABEL.NAME
        if nameKey in self.request.GET:
            queryset = queryset.filter(
                name__icontains=self.request.GET[nameKey])

        return queryset

    @extend_schema(parameters=[OpenApiParameter(name=PLAYLIST_ATTRIBUTES_LABEL.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL.TYPE,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        simplePlaylist = PlaylistService().CreateSimplePlaylist(
            self.request.user, self.request.data)
        
        responseSerializer = CriteriaPlaylistWithTracksSerializer(simplePlaylist)
        headers = self.get_success_headers(responseSerializer.data)
        return JsonResponse(
            data=responseSerializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(description=("""
                                Search within tracks, albums, artists and playlists.
                                The results is a set of four sets:
                                    - Playlist (searched and ordered by name);
                                    - Artist (searched and ordered by name);
                                    - Album (searched and ordered by name);
                                    - LibraryTrack (searched and ordered by title).
                                """))
    def get_querylist(self):
        querylist = (
            {
                'queryset': LibraryTrack.objects.all(),
                'serializer_class': TrackDetailedSerializer,
                'filter_fn': trackFilter},
            {
                'queryset': Playlist.objects.all(),
                'serializer_class': PlaylistWithoutTracksSerializer,
                'filter_fn': playlistFilter},
            {
                'queryset': Album.objects.all(),
                'serializer_class': AlbumWithoutTracksSerializer,
                'filter_fn': albumFilter},
            {
                'queryset': Artist.objects.all(),
                'serializer_class': ArtistDetailedSerializer,
                'filter_fn': artistFilter
            })

        return querylist