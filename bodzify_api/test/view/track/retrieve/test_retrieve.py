

import pytest
from rest_framework import status

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase
from bodzify_api.serializer.schema.lib_track.input.endpoint.post import Fields as PostFields


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_retrieve_track_then_ok(self):
        title = "We're All To Blame"
        data = {PostFields.TITLE: title}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        track_uuid = self.saved_lib_track.uuid

        response = self._retrieve_lib_track(lib_track_uuid=track_uuid)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_track_of_other_user_then_error(self):
        title = "We're All To Blame"
        data = {PostFields.TITLE: title}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        track_uuid = self.saved_lib_track.uuid

        response = self._retrieve_lib_track(lib_track_uuid=track_uuid)
        assert response.status_code == status.HTTP_200_OK

        self._login_as_test_user2()
        response = self._retrieve_lib_track(lib_track_uuid=track_uuid)
        assert response.status_code == status.HTTP_404_NOT_FOUND
