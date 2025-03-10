

from django.db.models import Q, QuerySet

from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter
from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import (
    PrivateUniqueResourceFilterSet
)
from bodzify_api.model.album.Album import Album
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.album.Fields import Fields as ModelFields

from .Fields import Fields


class AlbumFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(field_name=ModelFields.NAME_INTERNAL,
                                  field_name_public=ModelFields.NAME_PUBLIC,
                                  lookup_expr='icontains')
    album_artist_name = EmptiableCharFilter(
        field_name_public=Fields.ALBUM_ARTIST_NAME,
        method='filter_album_artist_name')

    class Meta:
        model = Album
        fields = [Fields.NAME_PUBLIC, Fields.ALBUM_ARTIST_NAME]

    def filter_album_artist_name(self, queryset: QuerySet, name, value):
        if value:
            filtered_qs = queryset.filter(
                Q(**{f'{ModelFields.ALBUM_ARTISTS}___{ArtistFields.NAME_PUBLIC}__icontains': value}))
            return filtered_qs
        else:
            return queryset.filter(album_artists__isnull=True)
