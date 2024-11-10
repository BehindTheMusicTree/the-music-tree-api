from typing import Optional, cast

from rest_framework import status

from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.serializer.schema.lib_track.input.endpoint.post import Fields
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_create_then_in_lib_track_mixin(self):
        title = "test"

        self._post_lib_track_with_generic_sample_no_tags(data_dict={Fields.TITLE: title})

        assert self.test_user1.all_lib_track_mixin.library_tracks.count() == 1
        lib_track = cast(Optional[LibraryTrack], self.test_user1.all_lib_track_mixin.library_tracks.first())
        assert lib_track
        assert lib_track.title == title
