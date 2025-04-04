from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_new_criteria_then_decrease_positions_of_following_tracks_in_old_criteria(self):
        old_genre = self.model_fixture_factory.create_genre(name="Metal")
        uploaded_track_following2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Lodwdw", genre=old_genre, use_manager_for_genre_playlist_adding=True)
        uploaded_track_following1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="cdss", genre=old_genre, use_manager_for_genre_playlist_adding=True)
        uploaded_track = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Love", genre=old_genre, use_manager_for_genre_playlist_adding=True)
        old_genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria=old_genre)
        assert old_genre_playlist.uploaded_track_playlist_rels.get(uploaded_track=uploaded_track).position == 1
        assert old_genre_playlist.uploaded_track_playlist_rels.get(
            uploaded_track=uploaded_track_following1).position == 2
        assert old_genre_playlist.uploaded_track_playlist_rels.get(
            uploaded_track=uploaded_track_following2).position == 3

        response = self._put_uploaded_track(uploaded_track.uuid, **{PutFields.GENRE: "Rock"})

        assert response.status_code == status.HTTP_200_OK
        old_genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria=old_genre)
        assert old_genre_playlist.uploaded_track_playlist_rels.get(
            uploaded_track=uploaded_track_following1).position == 1
        assert old_genre_playlist.uploaded_track_playlist_rels.get(
            uploaded_track=uploaded_track_following2).position == 2
