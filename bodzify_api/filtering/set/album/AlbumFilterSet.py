from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import \
    NonEmptiableCharFilter
from bodzify_api.filtering.filter.char.PrimaryFieldCharFilter import \
    PrimaryFieldCharFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import \
    PrivateUniqueResourceFilterSet
from bodzify_api.model.album.Album import Album
from bodzify_api.model.album.Fields import Fields as ModelFields
from bodzify_api.model.artist.Fields import Fields as ArtistModelFields

from .Fields import Fields


class AlbumFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(field_name=ModelFields.NAME_INTERNAL,
                                  field_name_user_friendly=ModelFields.NAME_PUBLIC,
                                  lookup_expr='icontains')
    album_artist_name = PrimaryFieldCharFilter(
        primary_field=ArtistModelFields.NAME_INTERNAL,
        field_name=ModelFields.ALBUM_ARTISTS,
        field_name_user_friendly=Fields.ALBUM_ARTIST_NAME,
        lookup_expr='icontains'
    )

    class Meta:
        model = Album
        fields = [Fields.NAME_PUBLIC, Fields.ALBUM_ARTIST_NAME]
