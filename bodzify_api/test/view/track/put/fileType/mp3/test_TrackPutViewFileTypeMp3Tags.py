#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewTestCaseFileTypeMp3Tags(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataFileTypeMp3Tags']
    sampleDirectoryRelativePath = "test/view/track/put/fileType/mp3/sample/"

    """
    On a mp3 file with uuid "36nS4LVDssLh4BvTARbJEK".
    The file had no metadata.
    All the following tags are set:
     - title;
     - artistName;
     - albumName;
     - albumArtistsName;
     - genreName;
     - rating;
     - language.
     Thus the corresponding tags in the mp3 file should be updated.
    """
    def test_trackPutFileTypeMp3TagsWhenPreviousHadAllTags(self):

        data = {
            "title": "Somewhere I Belong",
            "artistName": "Linkin Park",
            "albumName": "Meteora",
            "albumArtistsName": "Garou",
            "genreName": "LsjdqoqzpsdojEjGHGH", # "Rap"
            "rating": 10, # max value
            "language": "Peruvian"
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="36nS4LVDssLh4BvTARbJEK")
        trackMetadata = AudioMetadataService.GetMetadataDictFromFile(track)
        assert track.title == "Somewhere I Belong"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.TITLE] == "Somewhere I Belong"
        assert track.artist.name == "Linkin Park"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME] == "Linkin Park"
        assert track.album.name == "Meteora"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME] == "Meteora"
        assert track.album.name.albumArtists[0] == "Garou"
        assert trackMetadata[
                AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES] == "Garou"
        assert track.genre.name == "Rap"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME] == "Rap"
        assert track.rating == 10
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 255 # max id3 files
        assert track.language == "Peruvian"
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
     Thus the corresponding tags in the mp3 file should be updated.
    """
    def test_trackPutFileTypeMp3TagsWhenPreviousHadNoTag(self):

        data = {
            "title": "Somewhere I Belong",
            "artistName": "Linkin Park",
            "albumName": "Meteora",
            "albumArtistsName": "Garou",
            "genreName": "LsjdqoqzpsdojEjGHGH", # "Rap"
            "rating": 10, # max value
            "language": "Peruvian"
        }
        response = self._loginAndPutSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="36nS4LVDssLh4BvTAKKKKO")
        trackMetadata = AudioMetadataService.GetMetadataDictFromFile(track)
        assert track.title == "Somewhere I Belong"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.TITLE] == "Somewhere I Belong"
        assert track.artist.name == "Linkin Park"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME] == "Linkin Park"
        assert track.album.name == "Meteora"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME] == "Meteora"
        assert track.album.name.albumArtists[0] == "Garou"
        assert trackMetadata[
                AudioMetadataService.METADATA_DICT_KEYS.ALBUM_ARTISTS_NAMES] == "Garou"
        assert track.genre.name == "Rap"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME] == "Rap"
        assert track.rating == 10
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == 255 # max id3 files
        assert track.language == "Peruvian"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.LANGUAGE] == "Peruvian"
