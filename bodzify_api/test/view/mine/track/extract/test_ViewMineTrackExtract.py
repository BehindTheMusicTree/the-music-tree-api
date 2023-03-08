#!/usr/bin/env python
import os
from rest_framework import status
import bodzify_api.service.AudioMetadataService as AudioMetadataService
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
        MineTrackExtractViewTestCase)
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
from bodzify_api.model.track.LibraryTrack import LibraryTrack
import bodzify_api.settings as settings


class MineTrackExtractViewTestCase(MineTrackExtractViewTestCase):

    fixtures = ['initial_data', 'TestUserData']

    """
    Extract a mp3 file from myfreemp3:
    - the metadata specified in the post request (title, artist, 
    releasedOn) should be written in the file and set in the system;
    - the file extracted should be named "Jul_-_du_rap.mp3" as the artist is "Jul" and the title 
    is "du rap".
    - the extracted track should have no album as myfreemp3 doesn't provide this information;
    - the extracted track genre should be "Genreless" we don't provide one;
    information;
    - the extracted file should be stored in the test user's library.
    """
    def test_mineTrackExtrack(self):
        self._login(self.testUser)

        trackUrl = ("https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
        + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_KN414JidBi"
        + "kY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
            "title": "du rap",
            "artistName": "Jul",
            "releasedOn": 1290292
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(title="du rap")
        trackMetadata = AudioMetadataService.GetMetadataDictFromFile(
                file=track.file, appRatingMaxValue=settings.TRACK_RATING_MAX_VALUE)
        assert track.artist.name == "Jul"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_ARTIST_NAME_KEY] == "Jul"
        assert track.album == None
        assert trackMetadata[AudioMetadataService.METADATA_DICT_ALBUM_NAME_KEY] == None
        assert track.genre.name == CriteriaSpecialNames.GENRE_GENRELESS
        assert trackMetadata[AudioMetadataService.METADATA_DICT_GENRE_NAME_KEY] == None
        assert track.rating == None
        assert trackMetadata[AudioMetadataService.METADATA_DICT_RATING_KEY] == None
        assert track.file.name == self.testUserLibraryRelativePath + "Jul_-_du_rap.mp3"
        assert os.path.exists(settings.MEDIA_ROOT + track.file.name)
