from django_filters import NumberFilter, DateTimeFilter
from api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import (
    PrivateUniqueResourceFilterSet
)
from api.model.spotify_resource.children.artist.SpotifyArtist import SpotifyArtist
from api.model.spotify_resource.children.artist.Fields import Fields as ModelFields

from .Fields import Fields


class SpotifyArtistFilterSet(PrivateUniqueResourceFilterSet):
    name = NonEmptiableCharFilter(field_name=ModelFields.NAME,
                                  field_name_public=Fields.NAME_PUBLIC,
                                  lookup_expr='icontains')
    popularity_min = NumberFilter(field_name=ModelFields.POPULARITY, lookup_expr='gte')
    popularity_max = NumberFilter(field_name=ModelFields.POPULARITY, lookup_expr='lte')
    created_on = DateTimeFilter(field_name=ModelFields.CREATED_ON)
    created_on_gt = DateTimeFilter(field_name=ModelFields.CREATED_ON, lookup_expr='gt')
    created_on_lt = DateTimeFilter(field_name=ModelFields.CREATED_ON, lookup_expr='lt')
    created_on_gte = DateTimeFilter(field_name=ModelFields.CREATED_ON, lookup_expr='gte')
    created_on_lte = DateTimeFilter(field_name=ModelFields.CREATED_ON, lookup_expr='lte')
    updated_on = DateTimeFilter(field_name=ModelFields.UPDATED_ON)
    updated_on_gt = DateTimeFilter(field_name=ModelFields.UPDATED_ON, lookup_expr='gt')
    updated_on_lt = DateTimeFilter(field_name=ModelFields.UPDATED_ON, lookup_expr='lt')
    updated_on_gte = DateTimeFilter(field_name=ModelFields.UPDATED_ON, lookup_expr='gte')
    updated_on_lte = DateTimeFilter(field_name=ModelFields.UPDATED_ON, lookup_expr='lte')

    class Meta:
        model = SpotifyArtist
        fields = [
            ModelFields.NAME,
            ModelFields.POPULARITY,
            ModelFields.CREATED_ON,
            ModelFields.UPDATED_ON,
            *PrivateUniqueResourceFilterSet.get_date_fields()
        ]
