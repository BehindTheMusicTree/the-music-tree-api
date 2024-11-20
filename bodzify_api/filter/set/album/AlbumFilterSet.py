from django_filters import CharFilter
from django.db.models import Q, QuerySet

from bodzify_api.filter.EmptiableCharFilter import EmptiableCharFilter
from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.model.album.Album import Album
from bodzify_api.model.album.Fields import Fields as ModelFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from .Fields import Fields


class AlbumFilterSet(AppFilterSet):
    name = CharFilter(field_name=Fields.NAME, lookup_expr='icontains')
    album_artist_name = EmptiableCharFilter(method='filter_album_artist_name')

    class Meta:
        model = Album
        fields = [Fields.NAME, Fields.ALBUM_ARTIST_NAME]

    def filter_album_artist_name(self, queryset: QuerySet, name, value):
        if value == '':
            return queryset.filter(Q(album_artists__isnull=True))
        return queryset.filter(Q(**{f'{ModelFields.ALBUM_ARTISTS}__{ArtistFields.NAME}__icontains': value}))
