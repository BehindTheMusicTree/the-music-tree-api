from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.model.uploaded_track.input.post.Fields import Fields as PostFields
from bodzify_api.test.utils.uploaded_track.UploadedTrackTestFilename import UploadedTrackTestFilename
from bodzify_api.test.integration.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TestCase(UploadedTrackTestCase):

    def test_new_genre_then_first_position(self):
        genre_name = "Rock"
        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria__name=genre_name)
        assert genre_playlist.uploaded_track_playlist_rels.get(uploaded_track=self.saved_object).position == 1

    def test_existing_then_first_position_and_other_tracks_after(self):
        genre_name = "Rock"
        genre = self.model_fixture_factory.create_genre(name=genre_name)
        uploaded_track1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="We're All To Blame", genre=genre, use_manager_for_genre_playlist_adding=True)
        uploaded_track2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="We're All To Blame", genre=genre, use_manager_for_genre_playlist_adding=True)

        response = self._post_uploaded_track(
            UploadedTrackTestFilename.METADATA_NONE_MP3, **{PostFields.GENRE: genre_name})

        assert response.status_code == status.HTTP_201_CREATED
        genre_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(criteria__name=genre_name)
        assert genre_playlist.uploaded_track_playlist_rels.get(uploaded_track=self.saved_object).position == 1
        assert genre_playlist.uploaded_track_playlist_rels.get(uploaded_track=uploaded_track1).position == 3
        assert genre_playlist.uploaded_track_playlist_rels.get(uploaded_track=uploaded_track2).position == 2
