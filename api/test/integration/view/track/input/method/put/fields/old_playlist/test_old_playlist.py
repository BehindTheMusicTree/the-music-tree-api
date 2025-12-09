from rest_framework import status

from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.model.track.Fields import Fields as TrackFields
from api.serializer.model.track.input.put.Fields import Fields as PutFields
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_new_criteria_then_not_in_old_criteria_playlist_anymore(self):
        old_genre = self.model_fixture_factory.create_genre(name="Metal")
        data = {TrackFields.TITLE: "Love", TrackFields.GENRE: old_genre}
        track = self.model_fixture_factory.create_track_with_file(
            use_manager_for_genre_playlist_adding=True, **data)
        assert track in old_genre.criteria_playlist.tracks.all()

        new_genre_name = "Rock"
        response = self._put_track(track.uuid, **{PutFields.GENRE: new_genre_name})

        assert response.status_code == status.HTTP_200_OK
        old_genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria=old_genre)
        assert track not in old_genre_playlist.tracks.all()
