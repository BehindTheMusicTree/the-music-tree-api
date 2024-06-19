#!/usr/bin/env python

import pytest
from bodzify_api.test.view.track.TrackTestCase import TrackTestCase


@pytest.mark.django_db
class TestCase(TrackTestCase):

    """
    As the file is too big to be uploaded on Github, the pytest won't work during Github's
    actions. Therefore we have to comment this test before any dev push (as it triggers 
    Github actions)

    response = self.postSampleTrack(
        "post_Big_File 1-01 - Shine On You Crazy Diamond, Parts I–V.flac")
    assert response.status_code == status.HTTP_201_CREATED
    """

    def test_errorWhenTooBig(self):
        ""
