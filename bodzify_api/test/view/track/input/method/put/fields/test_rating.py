from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.put.Fields import \
    Fields as PutFields
from bodzify_api.test.utils.field.body_data.method.PutBodyDataTestCase import \
    PutBodyDataTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, PutBodyDataTestCase):

    def test_not_provided_then_unchanged(self):
        rating = 5
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Korinto", rating=rating)

        response = self._put_lib_track(uuid=lib_track.uuid, **{})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.rating == rating

    def test_zero(self):
        rating = 0
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Korinto")

        response = self._put_lib_track(uuid=lib_track.uuid, **{PutFields.RATING: rating})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.rating == rating
