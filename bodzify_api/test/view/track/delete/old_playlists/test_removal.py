
import pytest
from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(LibTrackTestCase):

    def test_delete_then_not_in_the_all_playlist(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title="We're All To Blame")
        all_tracks = self.test_user1.all_lib_track_mixin.all_tracks
        response = self._delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert track not in all_tracks.library_tracks.all()

    def test_delete_then_remove_from_the_genre_playlists(self):
        genre1_name = "Rock"
        genre1 = self.model_fixture_factory.create_genre(name=genre1_name)
        genre2_name = "Hard rock"
        genre2 = self.model_fixture_factory.create_genre(name=genre2_name, parent=genre1)
        genre3_name = "Emo"
        genre3 = self.model_fixture_factory.create_genre(name=genre3_name, parent=genre2)

        track = self.model_fixture_factory.create_lib_track_with_file(title="Love", genre=genre3)

        response = self._delete_lib_track(lib_track_uuid=track.uuid)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        criteria_playlist1: CriteriaPlaylist = genre1.criteria_playlist
        assert track not in criteria_playlist1.base_playlist.library_tracks.all()

        criteria_playlist2: CriteriaPlaylist = genre2.criteria_playlist
        assert track not in criteria_playlist2.base_playlist.library_tracks.all()

        criteria_playlist3: CriteriaPlaylist = genre3.criteria_playlist
        assert track not in criteria_playlist3.base_playlist.library_tracks.all()
