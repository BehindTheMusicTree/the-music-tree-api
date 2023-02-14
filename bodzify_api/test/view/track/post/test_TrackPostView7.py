import pytest
from rest_framework import status
from bodzify_api.test.view.track.post.TrackPostViewTestCase import TrackPostViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria


@pytest.mark.django_db
class TrackPostViewTestCase7(TrackPostViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/7/"

    def test_libraryTrackPost7(self):
        self.login(self.testUser)

        """
        - Genre 'foo' non existing
        """
        response = self.postSampleTrack("genre_foo_non_existing.mp3")
        assert response.status_code == status.HTTP_201_CREATED
        assert Criteria.objects.filter(user=self.testUser, name="Foo").exists()
