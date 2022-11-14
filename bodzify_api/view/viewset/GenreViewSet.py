#!/usr/bin/env python

from rest_framework import viewsets

from bodzify_api.serializer.GenreSerializer import GenreSerializer
from bodzify_api.models import Genre

NAME_FIELD = "name"
PARENT_FIELD = "parent"

class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def get_queryset(self):
        queryset = Genre.objects.all()
        name = self.request.query_params.get(NAME_FIELD)
        parentParameter = self.request.query_params.get(PARENT_FIELD)

        if parentParameter == "": parent = None
        else: parent = parentParameter

        if name is None: queryset = queryset.filter(parent=parent)
        else: queryset = queryset.filter(name__contains=name, parent=parent)
        
        return queryset