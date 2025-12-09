from rest_framework import status

from api.serializer.model.track.input.put.Fields import Fields as PutFields
from api.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase, PutBodyDataTestCase):

    def test_not_provided_then_unchanged(self):
        rating = 5
        track = self.model_fixture_factory.create_track_with_file(title="Korinto", rating=rating)

        response = self._put_track(uuid=track.uuid, **{PutFields.TITLE: "Wech"})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.rating == rating

    def test_provided_then_update(self):
        rating = 0
        track = self.model_fixture_factory.create_track_with_file(title="Korinto")

        response = self._put_track(uuid=track.uuid, **{PutFields.RATING: rating})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.rating == rating
