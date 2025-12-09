from typing import cast
from rest_framework import status

from api.model.track.Track import Track
from api.serializer.model.track.input.post.Fields import Fields
from api.test.utils.track.TrackTestFilename import TrackTestFilename
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_create_then_in_track_mixin(self):
        title = "test"
        response = self._post_track(TrackTestFilename.METADATA_NONE_MP3, **{Fields.TITLE: title})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.test_user1.all_tracks_mixin.tracks.count() == 1
        track = cast(Track | None,
                     self.test_user1.all_tracks_mixin.tracks_not_archived.first())
        assert track
        assert track.title == title
