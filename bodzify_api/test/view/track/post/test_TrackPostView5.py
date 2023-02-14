import pytest
from rest_framework import status
from bodzify_api.test.view.track.post.TrackPostViewTestCase import TrackPostViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCase5(TrackPostViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/5/"

    def test_libraryTrackPost5(self):
        self.login(self.testUser)

        """
         - mp3 
         - With all tags
        """
        response = self.postSampleTrack("with_all_tags.mp3")
        assert response.status_code == status.HTTP_201_CREATED
