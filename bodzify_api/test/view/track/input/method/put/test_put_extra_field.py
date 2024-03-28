#!/usr/bin/env python

from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_extra_field_then_error(self):
        track = G(LibraryTrack, user=self.test_user, title="Foire")
        data = {"nonExistingField": "oifjqoif"}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data) # type: ignore
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
