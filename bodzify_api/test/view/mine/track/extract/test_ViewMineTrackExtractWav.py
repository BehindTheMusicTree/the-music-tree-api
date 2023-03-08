#!/usr/bin/env python
from rest_framework import status
from bodzify_api.test.view.mine.track.MineTrackViewTestCase import (
        MineTrackExtractViewTestCase)


class MineTrackExtractViewTestTitle(MineTrackExtractViewTestCase):

    fixtures = ['initial_data', 'TestUserData']

    """
    Extract a Wav file.
    """
    def test_mineTrackExtractTitleMissing(self):
        self._login(self.testUser)

        trackUrl = ("https://hypeddit-gates-prod.s3.amazonaws.com/o7idvi_main?response-content-typ"
                + "e=application%2Foctet-stream&response-content-disposition=attachment%3B%20f"
                + "ilename%3D%22Sean%20%26%20Dee%20-%20Game%20Of%20Thrones%20Theme%20%28Reinte"
                + "rpretation%20Mix%29%20%5BPAF070%5D.wav%22&X-Amz-Content-Sha256=UNSIGNED-PAY"
                + "LOAD&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAXMST74SOXPZG2BF5"
                + "%2F20230226%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230226T232822Z&X-A"
                + "mz-SignedHeaders=host&X-Amz-Expires=6000&X-Amz-Signature=d17c81fe7472fab603"
                + "3a573383731d8edbfca9e33044e3d83c34e319e7fbfd80")
        data = {
            "url": trackUrl,
            "title": "Hey",
            "artistName": "Jul",
            "albumName": "Monsieur",
            "albumArtistsName": "Jul & Roméo Elvis",
            "genreName": "Hip-Hop",
            "rating": 5,
            "language": "fr"
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_200_OK
