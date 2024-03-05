#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class TestCase(ApiViewTestCase):

    def test_error_when_file_not_existing(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  title="Kobra",
                  duration=0)
        response = self.download_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_410_GONE  # type: ignore

    def test_ok(self):
        file_path_relative_to_media_dir = self.test_user_lib_path_relative_to_media_dir / "sample.mp3"
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(file_path_relative_to_media_dir),
                  title="We're All To Blame",
                  duration=0)
        response = self.download_lib_track(lib_track_uuid=track.uuid)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
