from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.put.put import Fields as PutFields
from bodzify_api.test.view.track.input.method.put.fields.NullableFieldTestCase import NullableFieldTestCase


class TestCase(NullableFieldTestCase):

    def test_not_empty_then_ok(self):
        language = "a"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(lib_track.uuid, **{PutFields.LANGUAGE: language})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == language

    def test_not_provided_then_unchanged(self):
        language = "French"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", language=language)

        response = self._put_lib_track(lib_track.uuid, **{})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == language

    def test_empty_then_none(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", language="French")

        response = self._put_lib_track(lib_track.uuid, **{PutFields.LANGUAGE: ""})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == None

    def test_not_none_then_update(self):
        language = "a"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love", language="French")

        response = self._put_lib_track(lib_track.uuid, **{PutFields.LANGUAGE: language})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.language == language
