import pytest
from rest_framework import status
from bodzify_api.test.view.track.post.TrackPostViewTestCase import TrackPostViewTestCase
from bodzify_api.model.track.LibraryTrack import LibraryTrack


@pytest.mark.django_db
class TrackPostViewTestCase2(TrackPostViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/2/"

    def test_libraryTrackPost2(self):
        self.login(self.testUser)

        """
        - No rating
        - FLAC
        """
        response = self.postSampleTrack("sample_without_rating.flac")
        assert response.status_code == status.HTTP_201_CREATED
        track = LibraryTrack.objects.get(title="Je suis sympa", user=self.testUser)
        assert track.rating == 0
