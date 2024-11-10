
from rest_framework import status

from bodzify_api.serializer.schema.lib_track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_not_provided_then_unchanged(self):
        rating = 5
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Korinto", rating=rating)
        response = self._put_lib_track(lib_track_uuid=lib_track.uuid, data_dict={})
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.rating == rating

    def test_zero(self):
        rating = 0
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Korinto")
        data = {PutFields.RATING: rating}
        response = self._put_lib_track(lib_track_uuid=lib_track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.rating == rating
