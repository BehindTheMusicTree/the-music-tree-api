#!/usr/bin/env python

from django.http import JsonResponse
from rest_framework import status
from drf_multiple_model.viewsets import ObjectMultipleModelAPIViewSet
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist, TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist, \
    TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.playlist.output.PlaylistGetParamSerializer import \
    ATTRIBUTES_LABEL as PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.criteria.output.CriteriaPlaylistWithTrackSerializer import \
    CriteriaPlaylistWithTracksSerializer
from bodzify_api.serializer.track.output.TrackDetailedSerializer import TrackDetailedSerializer
from bodzify_api.service.playlist.PlaylistService import PlaylistService
from bodzify_api.view.pagination.DefaultMultipleModelLimitOffsetPagination import \
    DefaultMultipleModelLimitOffsetPagination
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import \
    ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL


class PlaylistViewSet(ObjectMultipleModelAPIViewSet):

    pagination_class = DefaultMultipleModelLimitOffsetPagination
    serializers = {
        'default': CriteriaPlaylistWithTracksSerializer,
        'list':  CriteriaPlaylistWithTracksSerializer,
        'retrieve':  CriteriaPlaylistWithTracksSerializer,
    }

    def get_queryset(self):
        type_key = PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL.TYPE
        if type_key in self.request.GET:
            type_filter = self.request.GET[type_key]
            if type_filter == SIMPLE_PLAYLIST_TYPE_LABEL:
                queryset = SimplePlaylist.objects.filter(
                    playlist__user=self.request.user)
            elif type_filter == CRITERIA_PLAYLIST_TYPES_LABEL.GENRE:
                queryset = CriteriaPlaylist.objects.filter(
                    playlist__user=self.request.user, type_id=CRITERIA_TYPES_ID.GENRE)
            elif type_filter == CRITERIA_PLAYLIST_TYPES_LABEL.TAG:
                queryset = CriteriaPlaylist.objects.filter(
                    playlist__user=self.request.user, type_id=CRITERIA_TYPES_ID.TAG)
        else:
            queryset = CriteriaPlaylist.objects.filter(user=self.request.user)

            parent_uuid_param_key = CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT
            if parent_uuid_param_key not in self.request.GET:
                queryset = queryset | SimplePlaylist.objects.filter(playlist__user=self.request.user)
            else:
                queryset = queryset.filter(
                    parent__uuid=self.request.GET[parent_uuid_param_key])

        name_key = ATTRIBUTES_LABEL.NAME
        if name_key in self.request.GET:
            queryset = queryset.filter(
                name__icontains=self.request.GET[name_key])

        return queryset

    @extend_schema(parameters=[OpenApiParameter(name=ATTRIBUTES_LABEL.NAME,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY),
                               OpenApiParameter(name=PLAYLIST_GET_PARAM_ATTRIBUTES_LABEL.TYPE,
                                                type=OpenApiTypes.STR,
                                                location=OpenApiParameter.QUERY)])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        simple_playlist = PlaylistService().create_simple_playlist(
            self.request.user, self.request.data)

        response_serializer = CriteriaPlaylistWithTracksSerializer(simple_playlist)
        headers = self.get_success_headers(response_serializer.data)
        return JsonResponse(
            data=response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
