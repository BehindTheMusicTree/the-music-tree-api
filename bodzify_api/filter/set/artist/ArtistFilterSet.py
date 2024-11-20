from django_filters import CharFilter

from bodzify_api.filter.set.AppFilterSet import AppFilterSet
from bodzify_api.model.artist.Artist import Artist
from .Fields import Fields


class ArtistFilterSet(AppFilterSet):
    name = CharFilter(field_name=Fields.NAME, lookup_expr='icontains')

    class Meta:
        model = Artist
        fields = [Fields.NAME]
