import pytest
from rest_framework import status
from bodzify_api.test.view.track.post.TrackPostViewTestCase import TrackPostViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCase8(TrackPostViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/8/"

    def test_libraryTrackPost8(self):
        self.login(self.testUser)

        """
        - Wrong extension (mp4)
        """
        response = self.postSampleTrack("bad_extension.mp4")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
