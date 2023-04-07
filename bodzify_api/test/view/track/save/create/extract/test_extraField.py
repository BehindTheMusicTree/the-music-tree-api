#!/usr/bin/env python
from rest_framework import status

from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase


class ExtraFieldTestCase(TrackViewTestCase):

    def test_error(self):
        data = {
            "url": "https://lasonotheque.org/UPLOAD/wav/0001.wav",
            "fieldNotHandled": "pofkefposkfwp"
        }
        response = self.extract(data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
