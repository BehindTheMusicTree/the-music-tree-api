#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_extra_field_then_error(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="Foire")
        data = {"nonExistingField": "oifjqoif"}
        response = self._put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
