#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.criteria.input.schema.endpoint.CriteriaPostSerializer import FIELDS as POST_FIELDS
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_playlist_creation(self):
        genre_name = "Rock"
        data = {POST_FIELDS.NAME: genre_name}
        response = self.post_genre(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert CriteriaPlaylist.objects.filter(criteria__name=genre_name).exists()
