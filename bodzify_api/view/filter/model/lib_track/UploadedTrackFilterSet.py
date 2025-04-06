from django_filters import rest_framework as filters

from bodzify_api.model.uploaded_track.UploadedTrack import UploadedTrack
from bodzify_api.model.uploaded_track.Fields import Fields


class UploadedTrackFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name=Fields.NAME, lookup_expr='icontains')
    artist = filters.CharFilter(field_name=Fields.ARTIST, lookup_expr='icontains')
    album = filters.CharFilter(field_name=Fields.ALBUM, lookup_expr='icontains')
    genre = filters.CharFilter(field_name=Fields.GENRE, lookup_expr='icontains')
    tag = filters.CharFilter(field_name=Fields.TAG, lookup_expr='icontains')
    duration_min = filters.NumberFilter(field_name=Fields.DURATION_MS, lookup_expr='gte')
    duration_max = filters.NumberFilter(field_name=Fields.DURATION_MS, lookup_expr='lte')
    created_after = filters.DateTimeFilter(field_name=Fields.CREATED_AT, lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name=Fields.CREATED_AT, lookup_expr='lte')

    class Meta:
        model = UploadedTrack
        fields = [
            Fields.NAME,
            Fields.ARTIST,
            Fields.ALBUM,
            Fields.GENRE,
            Fields.TAG,
            Fields.DURATION_MS,
            Fields.CREATED_AT,
        ]
