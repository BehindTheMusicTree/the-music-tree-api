
from django_filters import CharFilter
from django.db.models import Q, QuerySet

from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.model.album.Album import Album
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.Artist import Fields as ArtistFields


class Fields:
    NAME = AlbumFields.NAME
    ALBUM_ARTISTS_NAME = f'{AlbumFields.ALBUM_ARTISTS}__{ArtistFields.NAME}'


class AlbumFilterSet(AppFilterSet):
    name = CharFilter(field_name=Fields.NAME, lookup_expr='icontains')
    album_artists_name = CharFilter(method=f'filter_{AlbumFields.ALBUM_ARTISTS}_{ArtistFields.NAME}')

    class Meta:
        model = Album
        fields = [
            Fields.NAME,
            Fields.ALBUM_ARTISTS_NAME
        ]

    def filter_album_artists_name(self, queryset: QuerySet, name, value):
        if value:
            return queryset.filter(
                Q(album_artists__isnull=False) &
                Q(**{f'{Fields.ALBUM_ARTISTS_NAME}__icontains': value})
            )
        return queryset
