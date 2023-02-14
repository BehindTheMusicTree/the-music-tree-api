import pytest
from rest_framework import status
from bodzify_api.test.view.track.post.TrackPostViewTestCase import TrackPostViewTestCase


@pytest.mark.django_db
class TrackPostViewTestCase9(TrackPostViewTestCase):

    fixtures = ['initial_data', 'TestUserData']
    sampleDirectoryRelativePath = "test/view/track/post/sample/9/"

    def test_libraryTrackPost9(self):
        self.login(self.testUser)

        """
        As the file is too big to be uploaded on Github, the pytest won't work during Github's
        actions. Therefore we have to comment this test before any dev push (as it triggers 
        Github actions)
        
        response = self.postSampleTrack(
            "post_Big_File 1-01 - Shine On You Crazy Diamond, Parts I–V.flac")
        assert response.status_code == status.HTTP_201_CREATED
        """