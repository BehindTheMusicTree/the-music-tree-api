#!/usr/bin/env python

from rest_framework.decorators import action
from rest_framework import status

from drf_spectacular.utils import extend_schema

from django.http import JsonResponse

from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackSerializer
from bodzify_api.serializer.track.LibraryTrackSerializer import LibraryTrackResponseSerializer
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.PlaylistType import PlaylistType, PlaylistTypeIds
from bodzify_api.view.viewset.MultiSerializerViewSet import MultiSerializerViewSet
from bodzify_api.dao import LibraryTrackDao
from bodzify_api.view import utility

GENRE_PARAM = "genre"

class LibraryTrackViewSet(MultiSerializerViewSet):
    queryset = LibraryTrack.objects.all()
    serializers = {
        'default': LibraryTrackSerializer,
        'list':  LibraryTrackResponseSerializer,
        'retrieve':  LibraryTrackResponseSerializer,
    }

    def get_queryset(self):
        queryset = LibraryTrack.objects.filter(user=self.request.user)
        genre = self.request.query_params.get(GENRE_PARAM)
        if genre is not None: queryset = queryset.filter(genre=genre)
        return queryset

    @extend_schema(
        request=LibraryTrackSerializer,
        responses=LibraryTrackResponseSerializer
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        track = self.get_object()
        oldGenre = LibraryTrack.objects.get(uuid=kwargs['pk']).genre
        requestSerializer = LibraryTrackSerializer(track, data=request.data, partial=partial)
        requestSerializer.is_valid(raise_exception=True)
        updatedTrack = requestSerializer.save()

        if oldGenre != updatedTrack.genre:
            newGenre = updatedTrack.genre

            genrePlaylistType = PlaylistType.objects.get(id=PlaylistTypeIds.GENRE)

            newGenreTreeItem = newGenre
            isNewGenreTreeItemInOldGenreTree = False

            while isNewGenreTreeItemInOldGenreTree is False:
                updatedTrack.playlists.add(Playlist.objects.get(
                    user=request.user,
                    type=genrePlaylistType,
                    criteria=newGenreTreeItem))
                newGenreTreeItem = newGenreTreeItem.parent

                oldGenreTreeItem = oldGenre
                while oldGenreTreeItem is not None and isNewGenreTreeItemInOldGenreTree is False:
                    isNewGenreTreeItemInOldGenreTree = (newGenreTreeItem == oldGenreTreeItem)
                    oldGenreTreeItem = oldGenreTreeItem.parent

            commonGenre = newGenreTreeItem
            oldGenreTreeItem = oldGenre

            while oldGenreTreeItem != commonGenre:
                updatedTrack.playlists.remove(Playlist.objects.get(
                    user=request.user,
                    type=genrePlaylistType,
                    criteria=oldGenreTreeItem))
                oldGenreTreeItem = oldGenreTreeItem.parent
            updatedTrack.save()

        LibraryTrackDao.updateTags(updatedTrack)

        serializer = LibraryTrackResponseSerializer(updatedTrack)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        return utility.GetFileResponseForTrackDownload(
            request=request, 
            track=LibraryTrackDao.get(uuid=pk))
        