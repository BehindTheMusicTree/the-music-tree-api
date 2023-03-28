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
    Extract a mp3 file with no genre specified. The genre should be set to "genreless" and the 
    tag should be empty.
    
    """
    def test_mineTrackExtrackGenreNone(self):
        trackUrl = (
                "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
                + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE_"
                + "KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        data = {
            "url": trackUrl,
            "title": "du rap"
        }
        response = self._loginAndExtract(data=data)
        assert response.status_code == status.HTTP_201_CREATED
        trackMetadata = AudioMetadataService.GetMetadataDictFromFile(
                file=self.savedTrack.file, 
                normalizedRatingMaxValue=settings.TRACK_RATING_MAX_VALUE)
        assert self.savedTrack.genre.name == CriteriaSpecialNames.GENRE_GENRELESS
        assert trackMetadata[AudioMetadataService.METADATA_DICT_KEYS.GENRE_NAME] in ['', None]
