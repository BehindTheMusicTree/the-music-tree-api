#!/usr/bin/env python

from rest_framework import status

from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_wav(self):
        response = self._post_lib_track_with_generic_sample_no_tags(extension='wav')
        assert response.status_code == status.HTTP_201_CREATED
        assert str(round(self.saved_lib_track.track_file.size_in_mo, 2)) == str(
            self.LibTrackGenericSamplesTagsNoneSizeInMo.WAV)

    def test_mp3(self):
        response = self._post_lib_track_with_generic_sample_no_tags(extension='mp3')
        assert response.status_code == status.HTTP_201_CREATED
        assert str(round(self.saved_lib_track.track_file.size_in_mo, 2)) == str(
            self.LibTrackGenericSamplesTagsNoneSizeInMo.MP3)

    def test_flac(self):
        response = self._post_lib_track_with_generic_sample_no_tags(extension='flac')
        assert response.status_code == status.HTTP_201_CREATED
        assert str(round(self.saved_lib_track.track_file.size_in_mo, 2)) == str(
            self.LibTrackGenericSamplesTagsNoneSizeInMo.FLAC)
