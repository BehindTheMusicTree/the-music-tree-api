from django.db.models import Q, QuerySet
from django_filters import CharFilter

from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import (
    PrivateUniqueResourceFilterSet
)
from bodzify_api.model.album.Fields import Fields as AlbumFields
from bodzify_api.model.artist.Fields import Fields as ArtistFields
from bodzify_api.model.criteria.Criteria import Fields as CriteriaFields
from bodzify_api.model.track.lib.Fields import Fields as ModelFields
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack

from .Fields import Fields


class LibTrackFilterSet(PrivateUniqueResourceFilterSet):
    title = CharFilter(field_name=ModelFields.TITLE, lookup_expr='icontains')
    artists_name = EmptiableCharFilter(
        field_name_public=f'artist_{ArtistFields.NAME_PUBLIC}', method=f'filter_artist_name')
    album_name = EmptiableCharFilter(
        field_name_public=f'{ModelFields.ALBUM}_{AlbumFields.NAME_PUBLIC}', method=f'filter_album_name')
    genre_name = EmptiableCharFilter(
        field_name_public=f'{ModelFields.GENRE}_{CriteriaFields.NAME_PUBLIC}', method=f'filter_genre_name')
    language = EmptiableCharFilter(
        field_name_public=ModelFields.LANGUAGE, field_name=ModelFields.LANGUAGE, lookup_expr='icontains')

    class Meta:
        model = LibraryTrack
        fields = [Fields.TITLE,
                  Fields.ARTISTS_NAME,
                  Fields.ALBUM_NAME,
                  Fields.GENRE_NAME,
                  Fields.LANGUAGE,]

    def filter_artist_name(self, queryset: QuerySet, name, value):
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
