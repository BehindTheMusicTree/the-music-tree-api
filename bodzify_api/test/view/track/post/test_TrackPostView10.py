import pytest
from rest_framework import status
from bodzify_api.test.view.track.post.TrackPostViewTestCase import TrackPostViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCase10(TrackPostViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/10/"

    def test_libraryTrackPost10(self):
        self.login(self.testUser)

        """
        - Wav file with no tag.
        """
        response = self.postSampleTrack("sample_without_tags.wav")
        assert response.status_code == status.HTTP_201_CREATED
