from api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import (
    PrivateUniqueResourceFilterSet
)
from api.model.artist.Artist import Artist

from .Fields import Fields


class ArtistFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(
        field_name=Fields.NAME_INTERNAL, field_name_public=Fields.NAME_PUBLIC, lookup_expr='icontains')

    class Meta:
        model = Artist
        fields = [
            Fields.NAME_PUBLIC,
            *PrivateUniqueResourceFilterSet.get_date_fields()
        ]
