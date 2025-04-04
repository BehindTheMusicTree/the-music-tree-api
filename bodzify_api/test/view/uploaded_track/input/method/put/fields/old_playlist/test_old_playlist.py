from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.uploaded_track.Fields import Fields as LibTrackFields
from bodzify_api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from bodzify_api.test.view.uploaded_track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_new_criteria_then_not_in_old_criteria_playlist_anymore(self):
        old_genre = self.model_fixture_factory.create_genre(name="Metal")
        data = {LibTrackFields.TITLE: "Love", LibTrackFields.GENRE: old_genre}
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            use_manager_for_genre_playlist_adding=True, **data)
        assert uploaded_track in old_genre.criteria_playlist.uploaded_tracks.all()

        new_genre_name = "Rock"
        response = self._put_uploaded_track(uploaded_track.uuid, **{PutFields.GENRE: new_genre_name})

        assert response.status_code == status.HTTP_200_OK
        old_genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria=old_genre)
        assert uploaded_track not in old_genre_playlist.uploaded_tracks.all()
