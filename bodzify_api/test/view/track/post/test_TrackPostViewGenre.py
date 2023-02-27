#!/usr/bin/env python
import pytest
from rest_framework import status
from bodzify_api.test.view.track.TrackViewTestCase import TrackViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria


@pytest.mark.django_db
class TrackPostViewTestCaseGenre(TrackViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/GenreNonExisting/"

    """
    Genre 'foo' non existing.
    """
    def test_libraryTrackPostGenreNonExisting(self):
        self.login(self.testUser)
        response = self.postSampleTrack("genre_foo_non_existing.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert Criteria.objects.filter(user=self.testUser, name="Foo").exists()
