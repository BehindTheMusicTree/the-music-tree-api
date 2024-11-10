from rest_framework import status

from .AllLibTracksMixinTestCase import AllLibTracksMixinTestCase

from bodzify_api.serializer.schema.lib_track.output.Fields import Fields as LibTrackOutputFields


class TestCase(AllLibTracksMixinTestCase):

    def test_get_then_one_result(self):
        self.model_fixture_factory.create_lib_track_with_file(title="test")
        self.model_fixture_factory.create_lib_track_with_file(title="test2")

        response = self._get_all_lib_tracks_mixin()

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 2

    def test_get_then_last_added_tracks_first(self):
        self._post_lib_track_with_generic_sample_no_tags()
        track_uuid_1 = self.saved_lib_track.uuid
        self._post_lib_track_with_generic_sample_no_tags()
        track_uuid_2 = self.saved_lib_track.uuid
        self._post_lib_track_with_generic_sample_no_tags()
        track_uuid_3 = self.saved_lib_track.uuid

        response = self._get_all_lib_tracks_mixin()

        assert response.status_code == status.HTTP_200_OK
        assert self.overall_total == 3
        assert self.results[0][LibTrackOutputFields.UUID] == track_uuid_3
        assert self.results[1][LibTrackOutputFields.UUID] == track_uuid_2
        assert self.results[2][LibTrackOutputFields.UUID] == track_uuid_1
