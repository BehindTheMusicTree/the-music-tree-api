#!/usr/bin/env python

from bodzify_api.serializers import GenreSerializer
from bodzify_api.models import Genre

from bodzify_api.viewset.BaseViewSet import BaseViewSet

NAME_FIELD = "name"
UUID_FIELD = "parent"

class GenreViewSet(BaseViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def create(self, request, *args, **kwargs):
        genreName = request.data[NAME_FIELD]
        if Genre.objects.filter(name=genreName).exists() == False:
            return super().create(request, *args, **kwargs) 
        return BaseViewSet.getHttpResponseWhenIssueWithBadRequest(request)