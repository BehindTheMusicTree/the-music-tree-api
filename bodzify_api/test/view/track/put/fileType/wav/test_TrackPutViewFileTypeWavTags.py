#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewTestCaseWavTags(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataFileTypeWav']
    sampleDirectoryRelativePath = "test/view/track/put/fileType/wav/sample/"

    """
    On a wav file with uuid "36nS4LVDssLh4BvTARbJEK".
    The file had no metadata.
    All the following tags are set:
     - title;
     - artistName;
     - albumName;
     - albumArtistsName;
     - genreName;
     - rating;
     - language.
    Thus the corresponding tags in the wav file should be updated.
    """
    def test_trackPutFileTypeWavTagsWhenPreviousHadNoTag(self):

        data = {
            "title": "Somewhere I Belong",
            "artistName": "Linkin Park",
            "albumName": "Meteora",
            "albumArtistsName": "Garou",
            "genreName": "Rap",
            "rating": 10,
            "language": "Peruvian"
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        trackMetadata = AudioMetadataService.GetMetadataDictFromFile(self.savedTrack.file)
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.TITLE] == "Somewhere I Belong"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME] == "Linkin Park"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME] == "Meteora"
        assert trackMetadata[
                AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES] == "Garou"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME] == "Rap"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 255
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE] == "Peruvian"
        

    """
    On a mp3 file with uuid "36nS4LVDssLh4BvTAKKKKO"
    All the following tags were set and are now updated:
     - title;
     - artistName;
     - albumName;
     - albumArtistsName;
     - genreName;
     - rating;
     - language.
    Thus the corresponding tags in the wav file should be updated.
    """
    def test_trackPutFileTypeWavTagsWhenPreviousHadAllTags(self):

        data = {
            "title": "Somewhere I Belong",
            "artistName": "Linkin Park",
            "albumName": "Meteora",
            "albumArtistsName": "Garou",
            "genreName": "Rap",
            "rating": 10,
            "language": "Peruvian"
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        trackMetadata = AudioMetadataService.GetMetadataDictFromFile(self.savedTrack.file)
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.TITLE] == "Somewhere I Belong"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME] == "Linkin Park"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME] == "Meteora"
        assert trackMetadata[
                AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES] == "Garou"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME] == "Rap"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 255
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE] == "Peruvian"
