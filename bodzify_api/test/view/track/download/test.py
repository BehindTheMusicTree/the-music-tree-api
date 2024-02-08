#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase


class DownloadTestCase(ApiViewTestCase):

    def test_errorWhenFileNotExisting(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Kobra",
                  duration=0)
        response = self.downloadTrack(trackUuid=track.uuid)
        assert response.status_code == status.HTTP_410_GONE

    def test_ok(self):
        filePathRelativeToMediaDir = self.test_user_library_path_relative_to_media_dir + "sample.mp3"
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=filePathRelativeToMediaDir,
                  title="We're All To Blame",
                  duration=0)
        response = self.downloadTrack(trackUuid=track.uuid)
        assert response.status_code == status.HTTP_200_OK
