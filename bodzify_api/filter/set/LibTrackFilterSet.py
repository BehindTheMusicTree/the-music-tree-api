from django_filters import CharFilter
from django.db.models import Q, QuerySet

from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.model.track.lib.Fields import Fields as ModelFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.criteria.Criteria import Fields as CriteriaFields


class Fields:
    TITLE = ModelFields.TITLE
    ARTISTS_NAME = f'{ModelFields.ARTISTS}__{ArtistFields.NAME}'
    ALBUM_NAME = f'{ModelFields.ALBUM}__{AlbumFields.NAME}'
    GENRE_NAME = f'{ModelFields.GENRE}__{CriteriaFields.NAME}'
    LANGUAGE = ModelFields.LANGUAGE


class LibTrackFilterSet(AppFilterSet):
    title = CharFilter(field_name=Fields.TITLE, lookup_expr='icontains')
    artists_name = CharFilter(method=f'filter_{ModelFields.ARTISTS}_{ArtistFields.NAME}')
    album_name = CharFilter(method=f'filter_{ModelFields.ALBUM}_{AlbumFields.NAME}')
    genre_name = CharFilter(method=f'filter_{ModelFields.GENRE}_{CriteriaFields.NAME}')
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

    def filter_artists_name(self, queryset: QuerySet, name, value):
        if value:
            return queryset.filter(
                Q(artists__isnull=False) &
                Q(**{f'{Fields.ARTISTS_NAME}__icontains': value})
            )
        return queryset

    def filter_album_name(self, queryset: QuerySet, name, value):
        if value:
            return queryset.filter(
                Q(album__isnull=False) &
                Q(**{f'{Fields.ALBUM_NAME}__icontains': value})
            )
        return queryset

    def filter_genre_name(self, queryset: QuerySet, name, value):
        if value:
            return queryset.filter(
                Q(genre__isnull=False) &
                Q(**{f'{Fields.GENRE_NAME}__icontains': value})
            )
        return queryset
