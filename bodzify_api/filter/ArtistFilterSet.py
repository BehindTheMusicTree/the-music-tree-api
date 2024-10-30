#!/usr/bin/env python

from django_filters import CharFilter

from bodzify_api.filter.AppFilterSet import AppFilterSet
from bodzify_api.model.Artist import Fields as ArtistFields, Artist


class Fields:
    NAME = ArtistFields.NAME


class ArtistFilterSet(AppFilterSet):
    name = CharFilter(field_name=Fields.NAME, lookup_expr='icontains')

    class Meta:
        model = Artist
        fields = [Fields.NAME]
