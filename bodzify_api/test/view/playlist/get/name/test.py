#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_NAME
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_withCustomNameShouldDisplayIt(self):
        daddysrockPlaylistCustomName = "Daddy's rock"
        rapGenre = G(Criteria,
                     user=self.testUser,
                     name="Hard rock",
                     type_id=CriteriaTypesId.GENRE)
        rapPlaylist = G(CriteriaPlaylist,
                        user=self.testUser,
                        type_id=CriteriaTypesId.GENRE,
                        customName=daddysrockPlaylistCustomName,
                        criteria=rapGenre)

        response = self.get(playlistUuid=rapPlaylist.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[
            PLAYLIST_ATTRIBUTES_NAME.NAME] == daddysrockPlaylistCustomName

    def test_withoutCustomNameShouldDisplayName(self):
        rockCriteriaName = "Rock"
        rockGenre = G(Criteria,
                      user=self.testUser,
                      name=rockCriteriaName,
                      type_id=CriteriaTypesId.GENRE)
        rockPlaylist = G(CriteriaPlaylist,
                         user=self.testUser,
                         type_id=CriteriaTypesId.GENRE,
                         criteria=rockGenre)

        response = self.get(playlistUuid=rockPlaylist.uuid)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[PLAYLIST_ATTRIBUTES_NAME.NAME] == rockCriteriaName
