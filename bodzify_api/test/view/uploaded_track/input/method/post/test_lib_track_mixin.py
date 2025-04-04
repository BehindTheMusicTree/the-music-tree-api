from typing import cast
from rest_framework import status

from bodzify_api.model.track.lib.LibraryTrack import UploadedTrack
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields
from bodzify_api.test.utils.uploaded_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_create_then_in_uploaded_track_mixin(self):
        title = "test"
        response = self._post_uploaded_track(LibTrackTestFilename.METADATA_NONE_MP3, **{Fields.TITLE: title})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.test_user1.all_uploaded_tracks_mixin.uploaded_tracks.count() == 1
        uploaded_track = cast(UploadedTrack | None,
                              self.test_user1.all_uploaded_tracks_mixin.uploaded_tracks_not_archived.first())
        assert uploaded_track
        assert uploaded_track.title == title
