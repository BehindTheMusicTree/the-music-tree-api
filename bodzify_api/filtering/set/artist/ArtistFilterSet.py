from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet \
    import PrivateUniqueResourceFilterSet
from bodzify_api.model.artist.Artist import Artist
from .Fields import Fields


class ArtistFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(field_name=Fields.NAME, lookup_expr='icontains')

    class Meta:
        model = Artist
        fields = [Fields.NAME]
