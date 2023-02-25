#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack
import bodzify_api.service.AudioMetadataService as AudioMetadataService


class TrackPutViewTestCaseFileFlac(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutDataFileFlac']
    sampleDirectoryRelativePath = "test/view/track/put/sample/FileFlac/"

    """
    On a wav file with uuid "36nS4LVDssLh4BvTARbJEK".
    The file had no metadata.
    All the following tags are set:
     - title;
     - artistName;
     - albumName;
     - albumArtistsNames;
     - genre;
     - rating;
     - language.
    Thus the corresponding tags in the flac file should be updated.
    """
    def test_trackPutFileFlacWhenPreviousHadAllTags(self):

        data = {
            "title": "Somewhere I Belong",
            "artistName": "Linkin Park",
            "albumName": "Meteora",
            "albumArtistsNames": "Garou",
            "genre": "LsjdqoqzpsdojEjGHGH", # "Rap"
            "rating": 10, # max value
            "language": "Peruvian"
        }
        response = self.putSampleTrack(trackUuid="36nS4LVDssLh4BvTARbJEK", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="36nS4LVDssLh4BvTARbJEK")
        trackMetadata = AudioMetadataService.GettrackMetadata(track)
        assert track.title == "Somewhere I Belong"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_TITLE_KEY] == "Somewhere I Belong"
        assert track.artist.name == "Linkin Park"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_ARTIST_NAME_KEY] == "Linkin Park"
        assert track.album.name == "Meteora"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_ALBUM_NAME_KEY] == "Meteora"
        assert track.genre.name == "Rap"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_GENRE_NAME_KEY] == "Rap"
        assert track.rating == 10
        assert trackMetadata[AudioMetadataService.METADATA_DICT_RATING_KEY] == 100 # max for Flac
        


    """
    On a mp3 file with uuid "36nS4LVDssLh4BvTAKKKKO"
    All the following tags were set and are now updated:
     - title;
     - artistName;
     - albumName;
     - albumArtistsNames;
     - genre;
     - rating;
     - language.
    Thus the corresponding tags in the flac file should be updated.
    """
    def test_trackPutFileFlacWhenPreviousHadNoTag(self):

        data = {
            "title": "Somewhere I Belong",
            "artistName": "Linkin Park",
            "albumName": "Meteora",
            "albumArtistsNames": "Garou",
            "genre": "LsjdqoqzpsdojEjGHGH", # "Rap"
            "rating": 10, # max value
            "language": "Peruvian"
        }
        response = self.putSampleTrack(trackUuid="36nS4LVDssLh4BvTAKKKKO", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="36nS4LVDssLh4BvTAKKKKO")
        trackMetadata = AudioMetadataService.GettrackMetadata(track)
        assert track.title == "Somewhere I Belong"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_TITLE_KEY] == "Somewhere I Belong"
        assert track.artist.name == "Linkin Park"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_ARTIST_NAME_KEY] == "Linkin Park"
        assert track.album.name == "Meteora"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_ALBUM_NAME_KEY] == "Meteora"
        assert track.genre.name == "Rap"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_GENRE_NAME_KEY] == "Rap"
        assert track.rating == 10
        assert trackMetadata[AudioMetadataService.METADATA_DICT_RATING_KEY] == 100 # max flac
        
