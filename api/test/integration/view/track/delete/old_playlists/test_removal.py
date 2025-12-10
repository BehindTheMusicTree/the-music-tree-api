from rest_framework import status

from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TrackDeleteViewTestCase(TrackTestCase):

    def test_delete_then_remove_from_the_genre_playlists(self):
        genre1_name = "Rock"
        genre1 = self.model_fixture_factory.create_genre(name=genre1_name)
        genre2_name = "Hard rock"
        genre2 = self.model_fixture_factory.create_genre(name=genre2_name, parent=genre1)
        genre3_name = "Emo"
        genre3 = self.model_fixture_factory.create_genre(name=genre3_name, parent=genre2)

        track = self.model_fixture_factory.create_track_with_file(title="Love", genre=genre3)

        response = self._delete_track(uuid=track.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        criteria_playlist1: CriteriaPlaylist = genre1.criteria_playlist
        assert track not in criteria_playlist1.tracks.all()

        criteria_playlist2: CriteriaPlaylist = genre2.criteria_playlist
        assert track not in criteria_playlist2.tracks.all()

        criteria_playlist3: CriteriaPlaylist = genre3.criteria_playlist
        assert track not in criteria_playlist3.tracks.all()
