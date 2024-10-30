#!/usr/bin/env python

from django_filters import CharFilter
from django.db.models import Q, QuerySet

from bodzify_api.filter.AppFilterSet import AppFilterSet
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.lib.Fields import Fields as ModelFields
from bodzify_api.model.Artist import Fields as ArtistFields
from bodzify_api.model.Album import Fields as AlbumFields
from bodzify_api.model.criteria.Criteria import Fields as CriteriaFields


class Fields:
    TITLE = ModelFields.TITLE
    ARTISTS_NAME = f'{ModelFields.ARTISTS}__{ArtistFields.NAME}'
    ALBUM_NAME = f'{ModelFields.ALBUM}__{AlbumFields.NAME}'
    GENRE_NAME = f'{ModelFields.GENRE}__{CriteriaFields.NAME}'
    LANGUAGE = ModelFields.LANGUAGE


class LibTrackFilterSet(AppFilterSet):
    title = CharFilter(field_name=Fields.TITLE, lookup_expr='icontains')
    artists_name = CharFilter(method=f'{ModelFields.ARTISTS}_{ArtistFields.NAME}_filter')
    album_name = CharFilter(method=f'{ModelFields.ALBUM}_{AlbumFields.NAME}_filter')
    genre_name = CharFilter(method=f'{ModelFields.GENRE}_{CriteriaFields.NAME}_filter')
    language = CharFilter(field_name=Fields.LANGUAGE, lookup_expr='icontains')

    class Meta:
        model = LibraryTrack
        fields = [
            Fields.TITLE,
            Fields.ARTISTS_NAME,
            Fields.ALBUM_NAME,
            Fields.GENRE_NAME,
            Fields.LANGUAGE,
        ]

    def artists_name_filter(self, queryset: QuerySet, name, value):
        if value:
            return queryset.filter(
                Q(artists__isnull=False) &
                Q(**{f'{Fields.ARTISTS_NAME}__icontains': value})
            )
        return queryset

    def album_name_filter(self, queryset: QuerySet, name, value):
        if value:
            return queryset.filter(
                Q(album__isnull=False) &
                Q(**{f'{Fields.ALBUM_NAME}__icontains': value})
            )
        return queryset

    def genre_name_filter(self, queryset: QuerySet, name, value):
        if value:
            return queryset.filter(
                Q(genre__isnull=False) &
                Q(**{f'{Fields.GENRE_NAME}__icontains': value})
            )
        return queryset
