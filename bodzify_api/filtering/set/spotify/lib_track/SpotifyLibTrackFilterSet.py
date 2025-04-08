from django_filters import NumberFilter, BooleanFilter, DateTimeFilter, CharFilter
from bodzify_api.filtering.filter.char.NonEmptiableCharFilter import NonEmptiableCharFilter
from bodzify_api.filtering.filter.char.RelatedObjectCharFilter import RelatedObjectCharFilter
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet import (
    PrivateUniqueResourceFilterSet
)
from bodzify_api.model.spotify.children.track.SpotifyLibTrack import SpotifyLibTrack
from bodzify_api.model.spotify.children.track.Fields import Fields as ModelFields
from bodzify_api.model.spotify.children.artist.Fields import Fields as ArtistModelFields

from .Fields import Fields


class SpotifyLibTrackFilterSet(PrivateUniqueResourceFilterSet):
    spotify_id = CharFilter(field_name=ModelFields.SPOTIFY_ID, lookup_expr='exact')
    name = NonEmptiableCharFilter(field_name=ModelFields.NAME,
                                  field_name_public=Fields.NAME_PUBLIC,
                                  lookup_expr='icontains')
    album_artist_name = RelatedObjectCharFilter(primary_field=ArtistModelFields.NAME,
                                                field_name=ModelFields.SPOTIFY_ARTISTS,
                                                field_name_public=Fields.ALBUM_ARTIST_NAME,
                                                lookup_expr='icontains')
    duration_sec_min = NumberFilter(method='filter_duration_sec_min')
    duration_sec_max = NumberFilter(method='filter_duration_sec_max')
    popularity_min = NumberFilter(field_name=ModelFields.POPULARITY, lookup_expr='gte')
    popularity_max = NumberFilter(field_name=ModelFields.POPULARITY, lookup_expr='lte')
    explicit = BooleanFilter(field_name=ModelFields.EXPLICIT)
    last_synced_at = DateTimeFilter(field_name=ModelFields.LAST_SYNCED_AT)
    last_synced_at_gt = DateTimeFilter(field_name=ModelFields.LAST_SYNCED_AT, lookup_expr='gt')
    last_synced_at_lt = DateTimeFilter(field_name=ModelFields.LAST_SYNCED_AT, lookup_expr='lt')
    last_synced_at_gte = DateTimeFilter(field_name=ModelFields.LAST_SYNCED_AT, lookup_expr='gte')
    last_synced_at_lte = DateTimeFilter(field_name=ModelFields.LAST_SYNCED_AT, lookup_expr='lte')
    is_removed = BooleanFilter(field_name=ModelFields.IS_REMOVED)

    def filter_duration_sec_min(self, queryset, name, value):
        return queryset.filter(**{f"{ModelFields.DURATION_MS}__gte": value * 1000})

    def filter_duration_sec_max(self, queryset, name, value):
        return queryset.filter(**{f"{ModelFields.DURATION_MS}__lte": value * 1000})

    class Meta:
        model = SpotifyLibTrack
        fields = [
            ModelFields.SPOTIFY_ID,
            ModelFields.NAME,
            ModelFields.SPOTIFY_ARTISTS,
            ModelFields.DURATION_MS,
            ModelFields.POPULARITY,
            ModelFields.EXPLICIT,
            ModelFields.LAST_SYNCED_AT,
            ModelFields.IS_REMOVED,
            *PrivateUniqueResourceFilterSet.get_date_fields()
        ]
