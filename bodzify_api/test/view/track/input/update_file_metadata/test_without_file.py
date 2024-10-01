#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.input.endpoint.post import Fields as PostFields
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_without_a_file_and_a_title_then_ok(self):
        track = self.model_fixture_factory.create_lib_track(title="Foire")
        data = {PostFields.TITLE: "Jobo"}
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
