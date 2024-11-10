
from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.lib_track.input.endpoint.extract import Fields as ExtractFields
from bodzify_api.test.view.track.input.save.FieldModelStrTestCase import FieldModelStrTestCase


class TestCase(FieldModelStrTestCase):

    def test_longest_then_ok(self):
        album_name = "a" * settings.ALBUM_NAME_LEN_MAX
        data = {ExtractFields.ALBUM_NAME: album_name}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album
        assert self.saved_lib_track.album.name == album_name

    def test_too_long_then_error(self):
        album_name = "a" * (settings.ALBUM_NAME_LEN_MAX + 1)
        data = {ExtractFields.ALBUM_NAME: album_name}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_empty_then_none(self):
        data = {ExtractFields.ALBUM_NAME: ''}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album == None

    def test_existing(self):
        album_name = "Kopoe"
        self.model_fixture_factory.create_album(name=album_name)
        data = {ExtractFields.ALBUM_NAME: album_name}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album
        assert self.saved_lib_track.album.name == album_name

    def test_not_existing(self):
        album_name = "hoho"
        data = {ExtractFields.ALBUM_NAME: album_name}
        response = self._post_lib_track_with_generic_sample_no_tags(data_dict=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_lib_track.album
        assert self.saved_lib_track.album.name == album_name
