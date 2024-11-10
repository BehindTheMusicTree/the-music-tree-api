import pytest
from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TestCase(LibTrackTestCase):

    def test_no_genre_then_in_genreless_playlists(self):
        response = self._post_lib_track_with_generic_sample_no_tags()

        assert response.status_code == status.HTTP_201_CREATED
        track_playlists = self.saved_lib_track.base_playlists.all()
        assert len(track_playlists) == 1
        track_criteria_playlists = CriteriaPlaylist.objects.filter(user=self.test_user1,
                                                                   base_playlist__in=track_playlists)
        assert track_criteria_playlists.filter(user=self.test_user1, criteria=None).exists()
