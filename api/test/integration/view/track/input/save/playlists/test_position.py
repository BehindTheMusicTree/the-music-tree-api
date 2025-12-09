from rest_framework import status

from api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from api.serializer.model.track.input.post.Fields import Fields as PostFields
from api.test.utils.track.TrackTestFilename import TrackTestFilename
from api.test.integration.view.track.TrackTestCase import TrackTestCase


class TestCase(TrackTestCase):

    def test_new_genre_then_first_position(self):
        genre_name = "Rock"
        response = self._post_track(
            TrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria__name=genre_name)
        assert genre_playlist.track_playlist_rels.get(track=self.saved_object).position == 1

    def test_existing_then_first_position_and_other_tracks_after(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        track1 = self.model_fixture_factory.create_track_with_file(
            title="We're All To Blame", genre=genre, use_manager_for_genre_playlist_adding=True)
        track2 = self.model_fixture_factory.create_track_with_file(
            title="We're All To Blame", genre=genre, use_manager_for_genre_playlist_adding=True)

        response = self._post_track(
            TrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria__name=genre_name)
        assert genre_playlist.track_playlist_rels.get(track=self.saved_object).position == 1
        assert genre_playlist.track_playlist_rels.get(track=track1).position == 3
        assert genre_playlist.track_playlist_rels.get(track=track2).position == 2
