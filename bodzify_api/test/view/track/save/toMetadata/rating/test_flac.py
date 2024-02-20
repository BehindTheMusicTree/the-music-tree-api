#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.AudioMetadataManager as AudioMetadataManager


class TestCase(ApiViewTestCase):

    def test_none(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": None,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] in [
            "", None]

    def test_zero(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": "0",
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 0

    def test_1_then_10(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "2Stars.flac"),
                  title="Love",
                  rating=4,
                  duration=0)
        data = {
            "rating": 1,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 10

    def test_2_then_20(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 2,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 20

    def test_3_then_30(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 3,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 30

    def test_4_then_40(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 4,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 40

    def test_5_then_50(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 5,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 50

    def test_6_then_60(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 6,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 60

    def test_7_then_70(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 7,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 70

    def test_8_then_80(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 8,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 80

    def test_9_then_90(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 9,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 90

    def test_10_then_100(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_library_abs_path / "1Star.flac"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 10,
        }
        response = self.put_sample_track(track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 100
