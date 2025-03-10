from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.put.Fields import Fields as PutFields
from bodzify_api.test.utils.field.body_data.method.PutBodyDataTestCase import PutBodyDataTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, PutBodyDataTestCase):

    def test_not_provided_then_unchanged(self):
        language = "Fr"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", language=language)

        response = self._put_lib_track(lib_track.uuid, **{PutFields.TITLE: 'MJ'})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == language

    def test_empty_then_none(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", language="Fr")

        response = self._put_lib_track(lib_track.uuid, **{PutFields.LANGUAGE: ""})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == None

    def test_provided_then_update(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", language="en")

        language = "fr"
        response = self._put_lib_track(lib_track.uuid, **{PutFields.LANGUAGE: language})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == language
