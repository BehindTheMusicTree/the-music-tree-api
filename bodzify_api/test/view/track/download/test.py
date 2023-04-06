#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class DownloadTestCase(TrackViewTestCase):

    def test_errorWhenFileNotExisting(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Kobra",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        response = self.downloadTrack(trackUuid=track.uuid)
        assert response.status_code == status.HTTP_410_GONE

    def test_ok(self):
        filePathRelativeToMediaDir = self.testUserLibraryPathRelativeToMediaDir + "sample.mp3"
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=filePathRelativeToMediaDir,
                  title="We're All To Blame",
                  genre=self.testUserGenrelessGenre,
                  duration=0)
        response = self.downloadTrack(trackUuid=track.uuid)
        assert response.status_code == status.HTTP_200_OK
