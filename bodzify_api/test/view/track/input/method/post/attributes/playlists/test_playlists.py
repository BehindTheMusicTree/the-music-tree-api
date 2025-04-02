from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.test.utils.lib_track.LibTrackTestFilename import LibTrackTestFilename
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_no_genre_then_in_genreless_playlists(self):
        response = self._post_lib_track(LibTrackTestFilename.METADATA_NONE_MP3)

        assert response.status_code == status.HTTP_201_CREATED
        track_playlists = self.saved_object.playlists.all()
        assert len(track_playlists) == 1
        track_criteria_playlists = CriteriaPlaylist.objects.filter(user=self.test_user1, playlist__in=track_playlists)
        assert track_criteria_playlists.filter(user=self.test_user1, criteria=None).exists()
