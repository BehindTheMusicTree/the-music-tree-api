#!/usr/bin/env python

from rest_framework import viewsets

from bodzify_api.serializers import GenreSerializer
from bodzify_api.models import Genre

import bodzify_api.viewset.utility as viewset_utility

NAME_FIELD = "name"
UUID_FIELD = "parent"

class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def create(self, request, *args, **kwargs):
        genreName = request.data[NAME_FIELD]
        if Genre.objects.filter(name=genreName).exists() == False:
            return super().create(request, *args, **kwargs) 
        return viewset_utility.GetHttpResponseWhenBadRequest(request)