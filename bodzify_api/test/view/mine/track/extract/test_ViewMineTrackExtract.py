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


    """
    Extract a mp3 file with specified data title and artist:
    - the metadata specified in the post request (title, artist, releasedOn) should be written in 
    the file and set in the system;
    - the file extracted should be named "Jul_-_du_rap.mp3" as the artist is "Jul" and the title 
    is "du rap".
    - the extracted track should have no album as it is not specified;
    - the extracted file should be stored in the test user's library.
    """
    def test_mineTrackExtrackWithTitleAndArtist(self):
        trackUrl = (
                "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
                + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_"
                + "KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        artistName = "Jul"
        title = "du rap"
        data = {
            "url": trackUrl,
            "title": title,
            "artistName": artistName,
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        trackMetadata = AudioMetadataService.GetMetadataDictFromFile(
                file=self.savedTrack.file, 
                normalizedRatingMaxValue=settings.TRACK_RATING_MAX_VALUE)
        assert self.savedTrack.artist.name == artistName
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.ARTIST_NAME] == artistName
        assert self.savedTrack.album == None
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.ALBUM_NAME] == None
        assert self.savedTrack.rating == None
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.RATING] == None
        filename = (artistName + " " + "-" + " " + title + ".mp3").replace(" ", "_")
        assert self.savedTrack.file.name == self.testUserLibraryRelativePath + filename
        assert os.path.exists(settings.MEDIA_ROOT + self.savedTrack.file.name)
