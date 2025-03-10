

from rest_framework import status

from bodzify_api.model.lib_track_playlist_rel.Fields import Fields as LibTrackPlaylistRelFields
from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.model.lib_track.input.put.Fields import Fields as PutFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_archived_lib_track_then_manual_playlist_has_plus_1_archived_lib_tracks(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name='teuf')

        track = self.model_fixture_factory.create_lib_track_with_file(title="not archived 1")
        self.model_fixture_factory.create_lib_track_playlist_rel(playlist=manual_playlist, lib_track=track)

        track_archived = self.model_fixture_factory.create_lib_track_with_file(title="archived 1", archived=True)
        self.model_fixture_factory.create_lib_track_playlist_rel(playlist=manual_playlist, lib_track=track_archived)

        response = self._put_lib_track(uuid=track.uuid, **{PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        manual_playlist_updated: ManualPlaylist = \
            ManualPlaylist.objects.get(user=self.test_user1, name=manual_playlist.name)
        assert manual_playlist_updated.lib_tracks_archived_count == 2
        assert manual_playlist_updated.lib_tracks_not_archived_count == 0

    def test_archived_lib_track_then_criteria_playlist_has_plus_1_archived_lib_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="rock")
        self.model_fixture_factory.create_lib_track_with_file(
            title="not archived 1", genre=criteria, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="archived 1", genre=criteria, archived=True, use_manager_for_genre_playlist_adding=True)
        track_love = self.model_fixture_factory.create_lib_track_with_file(
            title="Love", genre=criteria, use_manager_for_genre_playlist_adding=True)

        response = self._put_lib_track(uuid=track_love.uuid, **{PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre
        criteria_playlist_saved: CriteriaPlaylist = self.saved_object.genre.criteria_playlist
        assert criteria_playlist_saved.lib_tracks_archived_count == 2
        assert criteria_playlist_saved.lib_tracks_not_archived_count == 1

    def test_archived_lib_track_then_decrement_next_positions(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name="teuf")
        track1 = self.model_fixture_factory.create_lib_track_with_file(title="not archived 1")
        self.model_fixture_factory.create_lib_track_playlist_rel(playlist=manual_playlist.playlist, lib_track=track1)
        track2 = self.model_fixture_factory.create_lib_track_with_file(title="to archived 2")
        self.model_fixture_factory.create_lib_track_playlist_rel(playlist=manual_playlist.playlist, lib_track=track2)
        track3 = self.model_fixture_factory.create_lib_track_with_file(title="not archived 3")
        self.model_fixture_factory.create_lib_track_playlist_rel(playlist=manual_playlist.playlist, lib_track=track3)
        track4 = self.model_fixture_factory.create_lib_track_with_file(title="not archived 4")
        self.model_fixture_factory.create_lib_track_playlist_rel(playlist=manual_playlist.playlist, lib_track=track4)

        assert LibTrackPlaylistRel.objects.get(playlist=manual_playlist, lib_track=track1).position == 4
        assert LibTrackPlaylistRel.objects.get(playlist=manual_playlist, lib_track=track2).position == 3
        assert LibTrackPlaylistRel.objects.get(playlist=manual_playlist, lib_track=track3).position == 2
        assert LibTrackPlaylistRel.objects.get(playlist=manual_playlist, lib_track=track4).position == 1

        response = self._put_lib_track(uuid=track2.uuid, **{PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        manual_playlist_saved: ManualPlaylist = \
            ManualPlaylist.objects.get(user=self.test_user1, uuid=manual_playlist.uuid)
        assert manual_playlist_saved.lib_tracks_archived_count == 1
        assert manual_playlist_saved.lib_tracks_not_archived_count == 3

        lib_track_playlist_rels_not_archived: list[LibTrackPlaylistRel] = list(
            LibTrackPlaylistRel.objects.filter(
                user=self.test_user1, playlist=manual_playlist_saved, position__isnull=False
            ).order_by(LibTrackPlaylistRelFields.POSITION))
        assert lib_track_playlist_rels_not_archived[0].lib_track == track4
        assert lib_track_playlist_rels_not_archived[1].lib_track == track3
        assert lib_track_playlist_rels_not_archived[2].lib_track == track1
        archived_lib_track_playlist_rels = LibTrackPlaylistRel.objects.filter(
            user=self.test_user1, playlist=manual_playlist_saved, position__isnull=True)
        assert archived_lib_track_playlist_rels.count() == 1
        assert archived_lib_track_playlist_rels[0].lib_track == track2

    def test_unarchived_lib_track_then_in_first_position_of_playlist(self):
        manual_playlist_name = "manual playlist"
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name=manual_playlist_name)
        track1 = self.model_fixture_factory.create_lib_track_with_file(title="not archived 1")
        self.model_fixture_factory.create_lib_track_playlist_rel(playlist=manual_playlist, lib_track=track1)
        track2 = self.model_fixture_factory.create_lib_track_with_file(title="not archived 2")
        self.model_fixture_factory.create_lib_track_playlist_rel(playlist=manual_playlist, lib_track=track1)
        track3 = self.model_fixture_factory.create_lib_track_with_file(title="not archived 3")
        self.model_fixture_factory.create_lib_track_playlist_rel(playlist=manual_playlist, lib_track=track1)
        track4 = self.model_fixture_factory.create_lib_track_with_file(title="not archived 4")
        self.model_fixture_factory.create_lib_track_playlist_rel(playlist=manual_playlist, lib_track=track1)
        response = self._put_lib_track(uuid=track2.uuid, **{PutFields.ARCHIVED: "true"})
        assert response.status_code == status.HTTP_200_OK

        response = self._put_lib_track(uuid=track2.uuid, **{PutFields.ARCHIVED: "false"})

        assert response.status_code == status.HTTP_200_OK
        manual_playlist_saved: ManualPlaylist = \
            ManualPlaylist.objects.get(user=self.test_user1, name=manual_playlist_name)
        assert manual_playlist_saved.lib_tracks_archived_count == 0
        assert manual_playlist_saved.lib_tracks_not_archived_count == 4
        lib_track_playlist_rels_not_archived: list[LibTrackPlaylistRel] = list(
            LibTrackPlaylistRel.objects.filter(playlist=manual_playlist_saved, position__isnull=False)
            .order_by(LibTrackPlaylistRelFields.POSITION)
        )
        assert lib_track_playlist_rels_not_archived[0].lib_track == track2
        assert lib_track_playlist_rels_not_archived[1].lib_track == track4
        assert lib_track_playlist_rels_not_archived[2].lib_track == track3
        assert lib_track_playlist_rels_not_archived[3].lib_track == track1
