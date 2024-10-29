#!/usr/bin/env python

from django_filters import CharFilter
from django.db.models import Q, QuerySet

from bodzify_api.filter.AppFilterSet import AppFilterSet
from bodzify_api.model.Album import Album, Fields as AlbumFields
from bodzify_api.model.Artist import Fields as ArtistFields


class Fields:
    NAME = AlbumFields.NAME
    ALBUM_ARTISTS_NAME = f'{AlbumFields.ALBUM_ARTISTS}__{ArtistFields.NAME}'


class AlbumFilter(AppFilterSet):
    name = CharFilter(field_name=Fields.NAME, lookup_expr='icontains')
    album_artists_name = CharFilter(method=f'{AlbumFields.ALBUM_ARTISTS}_{ArtistFields.NAME}_filter')

    class Meta:
        model = Album
        fields = [
            Fields.NAME,
            Fields.ALBUM_ARTISTS_NAME
        ]

    def album_artists_name_filter(self, queryset: QuerySet, name, value):
        if value:
            return queryset.filter(
                Q(album_artists__isnull=False) &
                Q(**{f'{Fields.ALBUM_ARTISTS_NAME}__icontains': value})
            )
        return queryset
