from rest_framework import status

from bodzify_api.serializer.model.lib_track.input.put.Fields import     Fields as PutFields
from bodzify_api.test.utils.field.body_data.method.PutBodyDataTestCase import     PutBodyDataTestCase
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase, PutBodyDataTestCase):

    def test_not_provided_then_unchanged(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(uuid=track.uuid, **{PutFields.TITLE: "Love"})

        assert response.status_code == status.HTTP_200_OK
        assert not self.saved_object.archived

        track = self.model_fixture_factory.create_lib_track_with_file(title="Love", archived=True)

        response = self._put_lib_track(uuid=track.uuid, **{PutFields.TITLE: "Love"})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.archived

    def test_empty_then_error(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="Love")
        response = self._put_lib_track(uuid=track.uuid, **{PutFields.ARCHIVED: ''})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_not_boolean_then_error(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="Love")
        response = self._put_lib_track(uuid=track.uuid, **{PutFields.ARCHIVED: 'koko'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_true_then_update(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(uuid=track.uuid, **{PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.archived

    def test_true_in_capital_letters_then_update(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="Love")

        response = self._put_lib_track(uuid=track.uuid, **{PutFields.ARCHIVED: 'TRUE'})\

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.archived

    def test_false_then_update(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="Love", archived=True)

        response = self._put_lib_track(uuid=track.uuid, **{PutFields.ARCHIVED: "false"})

        assert response.status_code == status.HTTP_200_OK
        assert not self.saved_object.archived

    def test_false_in_capital_letters_then_update(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="Love", archived=True)

        response = self._put_lib_track(uuid=track.uuid, **{PutFields.ARCHIVED: 'FALSE'})

        assert response.status_code == status.HTTP_200_OK
        assert not self.saved_object.archived
