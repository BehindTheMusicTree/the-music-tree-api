#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api import settings
from bodzify_api.model.track.LibraryTrack import LibraryTrack, \
    ATTRIBUTES_LABEL as TRACK_ATTRIBUTES_LABEL
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_notProvidedThenUnchanged(self):
        title = "Mon Amour"
        track = G(LibraryTrack,
                  user=self.test_user,
                  title=title,
                  duration=0)
        data = {}
        response = self.put_sample_track(track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrack.title == title
