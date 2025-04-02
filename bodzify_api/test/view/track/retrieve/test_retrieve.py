from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_retrieve_then_ok(self):
        title = "We're All To Blame"
        track_uuid = self.model_fixture_factory.create_lib_track_with_file(title=title).uuid

        response = self._retrieve_lib_track(uuid=track_uuid)

        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_from_other_user_then_404(self):
        title = "We're All To Blame"
        track_uuid = self.model_fixture_factory.create_lib_track_with_file(title=title).uuid

        self._login_as_test_user2()
        response = self._retrieve_lib_track(uuid=track_uuid)
        self._login_as_test_user1()

        assert response.status_code == status.HTTP_404_NOT_FOUND
