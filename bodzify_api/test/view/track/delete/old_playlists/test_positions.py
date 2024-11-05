import pytest
from rest_framework import status

from bodzify_api.model.LibTrackPlaylistPositionRel import LibTrackPlaylistPositionRel
from bodzify_api.test.view.track.TrackTestCase import LibTrackTestCase


@pytest.mark.django_db
class TrackDeleteViewTestCase(LibTrackTestCase):

    def test_removal_then_next_tracks_in_playlist_decrease_position(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        track_old_position_3 = self.model_fixture_factory.create_lib_track_with_file(title="We're All To Blame",
                                                                                     genre=genre_rock)
        track_old_position_2 = self.model_fixture_factory.create_lib_track_with_file(title="Still Waiting",
                                                                                     genre=genre_rock)
        track_old_position_1 = self.model_fixture_factory.create_lib_track_with_file(title="The Hell Song",
                                                                                     genre=genre_rock)

        base_playlist = genre_rock.criteria_playlist.base_playlist

        response = self._delete_lib_track(lib_track_uuid=track_old_position_1.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        playlist_relations = LibTrackPlaylistPositionRel.objects.filter(base_playlist=base_playlist)
        assert len(playlist_relations) == 2
        assert playlist_relations.get(library_track=track_old_position_2).position == 1
        assert playlist_relations.get(library_track=track_old_position_3).position == 2
