from rest_framework import status

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.model.lib_track.input.post.Fields import Fields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


, cast


class TestCase(LibTrackTestCase):

    def test_create_then_in_lib_track_mixin(self):
        title = "test"
        response = self._post_lib_track_with_generic_sample_no_tags(**{Fields.TITLE: title})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.test_user1.all_lib_tracks_mixin.lib_tracks.count() == 1
        lib_track = cast(LibraryTrack | None, self.test_user1.all_lib_tracks_mixin.lib_tracks_not_archived.first())
        assert lib_track
        assert lib_track.title == title
