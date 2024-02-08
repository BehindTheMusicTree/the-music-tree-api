#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import ATTRIBUTES_LABEL as CRITERIA_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_notProvidedThenUnchanged(self):
        self.post_genre(data_json={CRITERIA_ATTRIBUTES_LABEL.NAME: "Rap"})
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.saved_genre,
                  duration=0)
        data = {}
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.genre.uuid == self.saved_genre.uuid
