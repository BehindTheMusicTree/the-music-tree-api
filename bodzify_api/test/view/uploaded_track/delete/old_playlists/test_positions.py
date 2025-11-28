from rest_framework import status

from bodzify_api.model.uploaded_track_playlist_rel.UploadedTrackPlaylistRel import UploadedTrackPlaylistRel
from bodzify_api.test.view.uploaded_track.UploadedTrackTestCase import UploadedTrackTestCase


class TrackDeleteViewTestCase(UploadedTrackTestCase):

    def test_removal_then_next_tracks_in_playlist_decrease_position(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        track_old_position_3 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="We're All To Blame", genre=genre_rock, use_manager_for_genre_playlist_adding=True)
        track_old_position_2 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Still Waiting", genre=genre_rock, use_manager_for_genre_playlist_adding=True)
        track_old_position_1 = self.model_fixture_factory.create_uploaded_track_with_file(
            title="The Hell Song", genre=genre_rock, use_manager_for_genre_playlist_adding=True)

        response = self._delete_uploaded_track(uuid=track_old_position_1.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        playlist_relations = UploadedTrackPlaylistRel.objects.filter(playlist=genre_rock.criteria_playlist)
        assert len(playlist_relations) == 2
        playlist_relation: UploadedTrackPlaylistRel = playlist_relations.get(uploaded_track=track_old_position_2)
        assert playlist_relation.position == 1
        playlist_relation = playlist_relations.get(uploaded_track=track_old_position_3)
        assert playlist_relation.position == 2
