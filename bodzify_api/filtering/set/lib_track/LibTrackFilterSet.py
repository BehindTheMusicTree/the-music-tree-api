from django_filters import CharFilter

from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter
from bodzify_api.filtering.filter.char.PrimaryFieldCharFilter import PrimaryFieldCharFilter
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
    artists_name = PrimaryFieldCharFilter(
        primary_field=ArtistFields.NAME_INTERNAL,
        field_name=ModelFields.ARTISTS,
        field_name_public=Fields.ARTISTS_NAME,
        lookup_expr='icontains'
    )
    album_name = PrimaryFieldCharFilter(
        primary_field=AlbumFields.NAME_INTERNAL,
        field_name=ModelFields.ALBUM,
        field_name_public=Fields.ALBUM_NAME,
        lookup_expr='icontains'
    )
    genre_name = PrimaryFieldCharFilter(
        primary_field=CriteriaFields.NAME_INTERNAL,
        field_name=ModelFields.GENRE,
        field_name_public=Fields.GENRE_NAME,
        lookup_expr='icontains'
    )
    language = EmptiableCharFilter(
        field_name_public=ModelFields.LANGUAGE, field_name=ModelFields.LANGUAGE, lookup_expr='icontains')

    class Meta:
        model = LibraryTrack
        fields = [
            Fields.TITLE,
            Fields.ARTISTS_NAME,
            Fields.ALBUM_NAME,
            Fields.GENRE_NAME,
            Fields.LANGUAGE,
            *PrivateUniqueResourceFilterSet.get_date_fields()
        ]
