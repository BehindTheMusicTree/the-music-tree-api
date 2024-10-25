#!/usr/bin/env python


import pytest
from rest_framework import status

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(TrackTestCase):

    def test_delete_then_delete_file(self):
        filename = "sample.mp3"
        track = self.model_fixture_factory.create_lib_track_with_file(title="We're All To Blame", filename=filename)
        assert self.test_user1.does_track_filename_exist_in_lib(filename)
        assert track.track_file.file
        response = self._delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not LibraryTrack.objects.filter(user=self.test_user1, uuid=track.uuid).exists()
        assert not self.test_user1.does_track_filename_exist_in_lib(filename)
