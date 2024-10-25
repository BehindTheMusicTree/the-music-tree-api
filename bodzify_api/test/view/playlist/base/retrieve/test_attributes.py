#!/usr/bin/env python

from rest_framework import status

from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.serializer.schema.playlist.base.output.detailed import Fields as RetrieveFields
from bodzify_api.test.view.playlist.base.BasePlaylistTestCase import BasePlaylistTestCase


class TestCase(BasePlaylistTestCase):

    def test_retrieve_simple_then_ok(self):
        name = 'cuisine'
        playlist_uuid = self.model_fixture_factory.create_manual_playlist(name=name).base_playlist.uuid

        response = self._retrieve(base_playlist_uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[RetrieveFields.NAME] == name

    def test_retrieve_genre_then_ok(self):
        name = 'rock'
        genre = self.model_fixture_factory.create_genre(name=name)
        playlist_uuid = BasePlaylist.objects.get(criteria_child_playlist__criteria=genre,
                                                 criteria_child_playlist__type=CriteriaTypesId.GENRE).uuid

        response = self._retrieve(base_playlist_uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[RetrieveFields.NAME] == name

    def test_retrieve_tag_then_ok(self):
        name = 'fr'
        genre = self.model_fixture_factory.create_tag(name=name)
        playlist_uuid = BasePlaylist.objects.get(criteria_child_playlist__criteria=genre,
                                                 criteria_child_playlist__type=CriteriaTypesId.TAG).uuid

        response = self._retrieve(base_playlist_uuid=playlist_uuid)
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result[RetrieveFields.NAME] == name
