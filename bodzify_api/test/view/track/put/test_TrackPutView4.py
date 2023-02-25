#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class TrackPutViewTestCase4(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData', 'TestViewTrackPutData4']

    def test_trackPut4(self):

        """
        - Title not specified so unchanged;
        - max rating 255;
        - weird language "French12ééù12";
        - the albumName is not specified so must be unchanged. Thus the albumArtistsNames field is
        ignored and the album's name must keep being "Love Don't Let Me Go";
        - the artist's name is specified and empty. Therefore the track has no artist anymore.
        - new genre "EDM".
        """
        data = {
            "artistName": "",
            "albumArtistsNames": "Queen",
            "genre": "L1ZG85munGytJb885DDJS7",
            "rating": 255,
            "language": "French12ééù12"
        }
        response = self.putSampleTrack(trackUuid="dyFYZTP3anyaUBcLDDDDDS", data=data)
        assert response.status_code == status.HTTP_200_OK
        track = LibraryTrack.objects.get(uuid="dyFYZTP3anyaUBcLDDDDDS")
        assert track.title == "Tricky"
        assert track.language == "French12ééù12"
        assert track.rating == 255
        assert track.album.name == "Love Don't Let Me Go"
        assert track.artist_id == None
        assert track.genre.name == "EDM"
