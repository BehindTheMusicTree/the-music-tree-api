from rest_framework import status

from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_extra_field_then_error(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="Foire")
        data = {"nonExistingField": "oifjqoif"}
        response = self._put_lib_track(uuid=track.uuid, data_dict=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
