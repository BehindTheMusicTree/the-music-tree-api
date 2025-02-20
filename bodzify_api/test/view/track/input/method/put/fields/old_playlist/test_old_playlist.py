from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.lib_track.input.put.put import Fields as PutFields
from bodzify_api.model.track.lib.Fields import Fields as LibTrackFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_new_criteria_then_not_in_old_criteria_playlist_anymore(self):
        old_genre = self.model_fixture_factory.create_genre(name="Metal")
        new_genre_name = "Rock"
        lib_track = self.model_fixture_factory.create_lib_track_with_file(
            **{LibTrackFields.TITLE: "Love", LibTrackFields.GENRE: old_genre.uuid})
        assert lib_track in old_genre.criteria_playlist.lib_tracks.all()

        response = self._put_lib_track(lib_track.uuid, **{PutFields.GENRE_NAME: new_genre_name})

        assert response.status_code == status.HTTP_200_OK
        old_genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria=old_genre)
        assert lib_track not in old_genre_playlist.lib_tracks.all()
