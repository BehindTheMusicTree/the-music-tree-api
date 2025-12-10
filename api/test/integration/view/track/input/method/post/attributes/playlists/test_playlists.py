from rest_framework import status

from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_no_genre_then_in_genreless_playlists(self):
        response = self._post_track()

        assert response.status_code == status.HTTP_201_CREATED
        track_playlists = self.saved_object.playlists.all()
        assert len(track_playlists) == 1
        track_criteria_playlists = CriteriaPlaylist.objects.filter(user=self.test_user1, playlist__in=track_playlists)
        assert track_criteria_playlists.filter(user=self.test_user1, criteria=None).exists()
