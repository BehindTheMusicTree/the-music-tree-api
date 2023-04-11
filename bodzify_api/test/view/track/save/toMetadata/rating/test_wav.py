#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TestCase(ApiViewTestCase):

    def test_null(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=None,
                  duration=0)
        data = {
            "rating": None,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] in [
            "", None]

    def test_zero(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": "0",
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 0

    def test_1Then13(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "2Stars.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=4,
                  duration=0)
        data = {
            "rating": 1,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 13

    def test_2Then1(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 2,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 1

    def test_3Then54(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 3,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 54

    def test_4Then64(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 4,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 64

    def test_5Then118(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 5,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 118

    def test_6Then128(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 6,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 128

    def test_7Then186(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 7,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 186

    def test_8Then196(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 8,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 196

    def test_9Then242(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 9,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 242

    def test_10Then255(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  file=self.testUserLibraryAbsPath + "1Star.wav",
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 10,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 255
