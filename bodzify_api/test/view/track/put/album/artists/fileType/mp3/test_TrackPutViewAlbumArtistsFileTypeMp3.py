#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewAlbumArtistsFileTypeMp3TestCase(TrackViewTestCase):
    
    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataAlbumArtistsFileTypeMp3']
    sampleDirectoryRelativePath = "test/view/track/put/album/artists/fileType/mp3/sample/"


    """
    null album artists. There shouldn't be a album artists tag in the file.
    """
    def test_trackPutAlbumFileTypeMp3None(self):
        data = {
            "albumName": "Chuck",
            "albumArtistsName": None
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, 
                AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES) in [None, ""]


    """
    The album artists is updated to a string of the highest length allowed.
    """
    def test_trackPutAlbumFileTypeMp3LongestString(self):
        data = {
            "albumName": "Chuck",
            "albumArtistsName": "a" * 100
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        assert AudioMetadataService.GetSpecificMetadataFromFile(
                self.savedTrack.file, 
                AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES) == "a" * 100
