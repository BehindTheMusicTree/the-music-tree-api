#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
import bodzify_api.AudioMetadataManager as AudioMetadataManager
from bodzify_api.test.view.track.input.update_file_metadata.rating.UpdateFileMetadataRatingTestCase import UpdateFileMetadataRatingTestCase


class TestCase(UpdateFileMetadataRatingTestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(file_extension='wav', value_max_in_metadata=255, methodName=methodName)

    def test_null(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=None,
                  duration=0)
        data = {
            "rating": None,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] in [
            "", None]

    def test_zero(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": "0",
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 0

    def test_1_then_13(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "2_stars.wav"),
                  title="Love",
                  rating=4,
                  duration=0)
        data = {
            "rating": 1,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 13

    def test_2_then_1(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 2,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 1

    def test_3_then_54(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 3,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 54

    def test_4_then_64(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 4,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 64

    def test_5_then_118(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 5,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 118

    def test_6_then_128(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 6,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 128

    def test_7_then_186(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 7,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 186

    def test_8_then_196(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 8,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 196

    def test_9_then_242(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 9,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 242

    def test_10_then_255(self):
        track = G(LibraryTrack,
                  user=self.test_user,
                  file=str(self.test_user_lib_abs_path / "1_star.wav"),
                  title="Love",
                  rating=2,
                  duration=0)
        data = {
            "rating": 10,
        }
        response = self.put_lib_track(lib_track_uuid=track.uuid, data_json=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track_metadata[AudioMetadataManager.METADATA_DICT_KEYS.RATING] == 255
