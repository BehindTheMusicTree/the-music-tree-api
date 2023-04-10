#!/usr/bin/env python
from rest_framework import status
from ddf import G
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ApiViewTestCase import ApiViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewRatingFileTypeFlacTestCase(ApiViewTestCase):

    def test_none(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
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

    def test_1Then10(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 1,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 10

    def test_2Then20(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=3,
                  duration=0)
        data = {
            "rating": 2,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 20

    def test_3Then30(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 3,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 30

    def test_4Then40(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 4,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 40

    def test_5Then50(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 5,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 50

    def test_6Then60(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 6,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 60

    def test_7Then70(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 7,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 70

    def test_8Then80(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 8,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 80

    def test_9Then90(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 9,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 90

    def test_10Then100(self):
        track = G(LibraryTrack,
                  user=self.testUser,
                  title="Love",
                  genre=self.testUserGenrelessGenre,
                  rating=2,
                  duration=0)
        data = {
            "rating": 10,
        }
        response = self.putSampleTrack(trackUuid=track.uuid, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.savedTrackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 100
