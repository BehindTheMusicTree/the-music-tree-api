
from bodzify_api.filtering.filter.char.EmptiableCharFilter import EmptiableCharFilter
from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet \
    import PrivateUniqueResourceFilterSet
from bodzify_api.model.album.Album import Album
from bodzify_api.model.album.Fields import Fields as ModelFields
from .Fields import Fields


class AlbumFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(field_name=ModelFields.NAME_INTERNAL,
                                  field_name_user_friendly=ModelFields.NAME,
                                  lookup_expr='icontains')
    album_artist_name = EmptiableCharFilter(lookup_expr='icontains')

    class Meta:
        model = Album
        fields = [Fields.NAME, Fields.ALBUM_ARTIST_NAME]
