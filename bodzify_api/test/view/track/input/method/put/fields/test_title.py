from rest_framework import status

from bodzify_api.serializer.schema.model.lib_track.input.endpoint.put import Fields as PutFields
from bodzify_api.test.view.track.input.method.put.fields.NotNullableFieldTestCase import NotNullableFieldTestCase


class TestCase(NotNullableFieldTestCase):

    def test_not_empty_then_ok(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        title_new = "a"
        response = self._put_lib_track(lib_track.uuid, **{PutFields.TITLE: title_new})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.title == title_new

    def test_not_provided_then_unchanged(self):
        old_title = "Love"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title=old_title)

        response = self._put_lib_track(lib_track.uuid, **{})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.title == old_title

    def test_empty_then_error(self):
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(lib_track.uuid, **{PutFields.TITLE: ""}
                                       )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_none_then_update(self):
        title = "a"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(title=title)

        response = self._put_lib_track(lib_track.uuid, **{PutFields.TITLE: title})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_lib_track.title == title
