from rest_framework import status

from api.serializer.model.track.input.Fields import Fields as PutFields
from api.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase, PutBodyDataTestCase):

    def test_not_provided_then_unchanged(self):
        language = "Fr"
        track = self.model_fixture_factory.create_track_with_file(title="Love", language=language)

        response = self._put_track(track.uuid, **{PutFields.TITLE: 'MJ'})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == language

    def test_empty_then_none(self):
        track = self.model_fixture_factory.create_track_with_file(title="Love", language="Fr")

        response = self._put_track(track.uuid, **{PutFields.LANGUAGE: ""})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == None

    def test_provided_then_update(self):
        track = self.model_fixture_factory.create_track_with_file(title="Love", language="en")

        language = "fr"
        response = self._put_track(track.uuid, **{PutFields.LANGUAGE: language})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == language
