

from typing import cast
from rest_framework import status
from django.db.models import QuerySet

from bodzify_api.model.uploaded_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.model.uploaded_track.input.put.Fields import Fields as PutFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_archived_uploaded_track_then_manual_playlist_has_plus_1_archived_uploaded_tracks(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name='teuf')

        track = self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 1")
        self.model_fixture_factory.create_uploaded_track_playlist_rel(playlist=manual_playlist, uploaded_track=track)

        track_archived = self.model_fixture_factory.create_uploaded_track_with_file(title="archived 1", archived=True)
        self.model_fixture_factory.create_uploaded_track_playlist_rel(
            playlist=manual_playlist, uploaded_track=track_archived)

        response = self._put_uploaded_track(uuid=track.uuid, **{PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        manual_playlist_updated: ManualPlaylist = \
            ManualPlaylist.objects.get(user=self.test_user1, name=manual_playlist.name)
        assert manual_playlist_updated.uploaded_tracks_archived_count == 2
        assert manual_playlist_updated.uploaded_tracks_not_archived_count == 0

    def test_archived_uploaded_track_then_criteria_playlist_has_plus_1_archived_uploaded_tracks(self):
        criteria = self.model_fixture_factory.create_genre(name="rock")
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="not archived 1", genre=criteria, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_uploaded_track_with_file(
            title="archived 1", genre=criteria, archived=True, use_manager_for_genre_playlist_adding=True)
        track_love = self.model_fixture_factory.create_uploaded_track_with_file(
            title="Love", genre=criteria, use_manager_for_genre_playlist_adding=True)

        response = self._put_uploaded_track(uuid=track_love.uuid, **{PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.genre
        criteria_playlist_saved: CriteriaPlaylist = self.saved_object.genre.criteria_playlist
        assert criteria_playlist_saved.uploaded_tracks_archived_count == 2
        assert criteria_playlist_saved.uploaded_tracks_not_archived_count == 1

    def test_archived_uploaded_track_then_decrement_next_positions(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name="teuf")
        track1 = self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 1")
        self.model_fixture_factory.create_uploaded_track_playlist_rel(
            playlist=manual_playlist.playlist, uploaded_track=track1)
        track_to_archive = self.model_fixture_factory.create_uploaded_track_with_file(title="to archived 2")
        self.model_fixture_factory.create_uploaded_track_playlist_rel(
            playlist=manual_playlist.playlist, uploaded_track=track_to_archive)
        track3 = self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 3")
        self.model_fixture_factory.create_uploaded_track_playlist_rel(
            playlist=manual_playlist.playlist, uploaded_track=track3)
        track4 = self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 4")
        self.model_fixture_factory.create_uploaded_track_playlist_rel(
            playlist=manual_playlist.playlist, uploaded_track=track4)

        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[1] == track4
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[2] == track3
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[3] == track_to_archive
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[4] == track1

        response = self._put_uploaded_track(uuid=track_to_archive.uuid, **{PutFields.ARCHIVED: "true"})

        assert response.status_code == status.HTTP_200_OK

        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[1] == track4
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[2] == track3
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[3] == track1

        archived_uploaded_track_playlist_rels = LibTrackPlaylistRel.objects.filter(
            user=self.test_user1, playlist=manual_playlist, position__isnull=True)
        assert archived_uploaded_track_playlist_rels.count() == 1
        assert cast(LibTrackPlaylistRel, archived_uploaded_track_playlist_rels.first()
                    ).uploaded_track == track_to_archive

    def test_unarchived_uploaded_track_then_in_first_position_of_playlist(self):
        manual_playlist = self.model_fixture_factory.create_manual_playlist(name="Cuisine")
        track1 = self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 1")
        self.model_fixture_factory.create_uploaded_track_playlist_rel(playlist=manual_playlist, uploaded_track=track1)
        track_to_unarchive = self.model_fixture_factory.create_uploaded_track_with_file(title="to unarchive")
        self.model_fixture_factory.create_uploaded_track_playlist_rel(
            playlist=manual_playlist, uploaded_track=track_to_unarchive)
        track3 = self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 3")
        self.model_fixture_factory.create_uploaded_track_playlist_rel(playlist=manual_playlist, uploaded_track=track3)
        track4 = self.model_fixture_factory.create_uploaded_track_with_file(title="not archived 4")
        self.model_fixture_factory.create_uploaded_track_playlist_rel(playlist=manual_playlist, uploaded_track=track4)

        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[1] == track4
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[2] == track3
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[3] == track_to_unarchive
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[4] == track1

        response = self._put_uploaded_track(uuid=track_to_unarchive.uuid, **{PutFields.ARCHIVED: "true"})
        assert response.status_code == status.HTTP_200_OK

        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[1] == track4
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[2] == track3
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[3] == track1

        uploaded_track_playlist_rels_of_playlist_archived: QuerySet[LibTrackPlaylistRel] = \
            LibTrackPlaylistRel.objects.filter(user=self.test_user1, playlist=manual_playlist, position__isnull=True)
        assert uploaded_track_playlist_rels_of_playlist_archived.count() == 1
        assert cast(LibTrackPlaylistRel, uploaded_track_playlist_rels_of_playlist_archived.first()
                    ).uploaded_track == track_to_unarchive

        response = self._put_uploaded_track(uuid=track_to_unarchive.uuid, **{PutFields.ARCHIVED: "false"})

        assert response.status_code == status.HTTP_200_OK

        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[1] == track_to_unarchive
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[2] == track4
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[3] == track3
        assert manual_playlist.uploaded_tracks_not_archived_dict_by_position[4] == track1

        assert LibTrackPlaylistRel.objects.filter(
            user=self.test_user1, playlist=manual_playlist, position__isnull=True).count() == 0
