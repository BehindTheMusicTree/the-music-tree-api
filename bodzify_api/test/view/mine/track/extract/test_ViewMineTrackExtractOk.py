#!/usr/bin/env python
import os
from rest_framework import status
import bodzify_api.service.AudioMetadataService as AudioMetadataService
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
        MineTrackExtractViewTestCase)
from bodzify_api.model.criteria.Criteria import CriteriaSpecialNames
import bodzify_api.settings as settings


class MineTrackExtractViewTestCaseUsual(MineTrackExtractViewTestCase):

    """
    Extract a mp3 file from myfreemp3:
    - the metadata specified in the post request (title, artist, releasedOn) should be written in
    the file and set in the system;
    - the file extracted should be named "Jul_-_du_rap.mp3" as the artist is "Jul" and the title 
    is "du rap".
    - the extracted track should have no album as myfreemp3 doesn't provide this information;
    - the extracted track genre should be "Genreless" we don't provide one;
    information;
    - the extracted file should be stored in the test user's library.
    """
    def test_mineTrackExtrackOk(self):
        
        trackUrl = ("https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
        + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_KN414JidBi"
        + "kY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
            "title": "du rap",
            "artistName": "Jul",
            "releasedOn": 1290292
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        trackMetadata = AudioMetadataService.GetMetadataDictFromFile(
                file=self.savedTrack.file, normalizedRatingMaxValue=settings.TRACK_RATING_MAX_VALUE)
        assert self.savedTrack.artist.name == "Jul"
        assert trackMetadata[AudioMetadataService.METADATA_DICT_ARTIST_NAME_KEY] == "Jul"
        assert self.savedTrack.album == None
        assert trackMetadata[AudioMetadataService.METADATA_DICT_ALBUM_NAME_KEY] == None
        assert self.savedTrack.genre.name == CriteriaSpecialNames.GENRE_GENRELESS
        assert trackMetadata[AudioMetadataService.METADATA_DICT_GENRE_NAME_KEY] == None
        assert self.savedTrack.rating == None
        assert trackMetadata[AudioMetadataService.METADATA_DICT_RATING_KEY] == None
        assert self.savedTrack.file.name == self.testUserLibraryRelativePath + "Jul_-_du_rap.mp3"
        assert os.path.exists(settings.MEDIA_ROOT + self.savedTrack.file.name)
