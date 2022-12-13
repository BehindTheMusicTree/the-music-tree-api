from rest_framework import status

from django.urls import reverse

from bodzify_api.test.view.ViewTestCase import ViewTestCase
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.Playlist import PlaylistSpecialNames


class LibraryTrackPutViewTestCase(ViewTestCase):

    def setUp(self) -> None:
        return super().setUp(sampleRelativePath="test/view/track/library/put/sample/")

    def test_libraryTrackPut(self):
        self.login(self.testUser)

        # assert [Playlist.objects.get(
        #     user=self.testUser,
        #     name="French cloud rap"
        # ) for val in track.playlists.all() if val in track.playlists.all()] is not []
