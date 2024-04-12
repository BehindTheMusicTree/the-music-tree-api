#!/usr/bin/env python

from dbm.ndbm import library
from pickle import FALSE
from rest_framework import status
from ddf import G
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.criteria.CriteriaType import CRITERIA_TYPES_ID
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.CriteriaPutSerializer import FIELDS as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_new_parent_then_tracks_in_same_order_and_added_at_the_beginning(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        rock_playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist
        lib_track_previously_second_in_rock = G(LibraryTrack, user=self.test_user, genre=rock_genre, title="kok")
        lib_track_previously_first_in_rock = G(LibraryTrack, user=self.test_user, genre=rock_genre, title="lkdw")

        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        lib_track_previously_second_in_punk = G(LibraryTrack, user=self.test_user, genre=punk_genre, title="punk song")
        lib_track_previously_first_in_punk = G(LibraryTrack, user=self.test_user, genre=punk_genre, title="loul")

        data = {PUT_FIELD.PARENT: rock_genre.uuid}  # type: ignore
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore

        playlist_lib_track_relation_relations = PlaylistLibTrackRelation.objects.filter(playlist=rock_playlist)
        assert playlist_lib_track_relation_relations.get(
            library_track=lib_track_previously_first_in_punk).position == 1  # type: ignore
        assert playlist_lib_track_relation_relations.get(
            library_track=lib_track_previously_second_in_punk).position == 2  # type: ignore
        assert playlist_lib_track_relation_relations.get(
            library_track=lib_track_previously_first_in_rock).position == 3  # type: ignore
        assert playlist_lib_track_relation_relations.get(
            library_track=lib_track_previously_second_in_rock).position == 4  # type: ignore

    def test_new_parent_then_tracks_in_same_order_and_added_at_the_beginning_of_parent_of_parent(self):
        guitare_genre = G(Criteria, name="Guitare", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        guitare_playlist = CriteriaPlaylist.objects.get(criteria=guitare_genre).playlist
        lib_track_previously_second_in_guitare = G(
            LibraryTrack, user=self.test_user, genre=guitare_genre, title="guitare2")
        lib_track_previously_first_in_guitare = G(
            LibraryTrack, user=self.test_user, genre=guitare_genre, title="guitare1")

        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=guitare_genre)
        lib_track_previously_second_in_rock = G(LibraryTrack, user=self.test_user, genre=rock_genre, title="rock2")
        lib_track_previously_first_in_rock = G(LibraryTrack, user=self.test_user, genre=rock_genre, title="rock1")

        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        lib_track_previously_second_in_punk = G(LibraryTrack, user=self.test_user, genre=punk_genre, title="punk2")
        lib_track_previously_first_in_punk = G(LibraryTrack, user=self.test_user, genre=punk_genre, title="punk1")

        data = {PUT_FIELD.PARENT: rock_genre.uuid}  # type: ignore
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore

        playlist_lib_track_relation_relations = PlaylistLibTrackRelation.objects.filter(playlist=guitare_playlist)
        tracks_positions = {relation.library_track.uuid: relation.position
                            for relation in playlist_lib_track_relation_relations}
        assert tracks_positions[lib_track_previously_first_in_punk.uuid] == 1  # type: ignore
        assert tracks_positions[lib_track_previously_second_in_punk.uuid] == 2  # type: ignore
        assert tracks_positions[lib_track_previously_first_in_rock.uuid] == 3  # type: ignore
        assert tracks_positions[lib_track_previously_second_in_rock.uuid] == 4  # type: ignore
        assert tracks_positions[lib_track_previously_first_in_guitare.uuid] == 5  # type: ignore
        assert tracks_positions[lib_track_previously_second_in_guitare.uuid] == 6  # type: ignore

    def test_new_parent_not_acendant_of_old_parent_then_update_positions_in_old_parent(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        rock_playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).playlist

        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=rock_genre)

        track_fourth_in_rock = G(LibraryTrack, user=self.test_user, genre=rock_genre, title="Rock song 2")
        G(LibraryTrack, user=self.test_user, genre=punk_genre, title="Punk song 2")
        track_second_in_rock = G(LibraryTrack, user=self.test_user, genre=rock_genre, title="Rock song")
        G(LibraryTrack, user=self.test_user, genre=punk_genre, title="Punk song")

        data = {PUT_FIELD.PARENT: ''}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore

        playlist_lib_track_relation_relations = PlaylistLibTrackRelation.objects.filter(playlist=rock_playlist)
        tracks_positions = {relation.library_track.uuid: relation.position
                            for relation in playlist_lib_track_relation_relations}
        assert tracks_positions[track_second_in_rock.uuid] == 1  # type: ignore
        assert tracks_positions[track_fourth_in_rock.uuid] == 2  # type: ignore

    def test_new_parent_undirect_ascendant_of_old_parent_then_update_positions_in_criterias_in_between(self):
        rock_genre = G(Criteria, name="Rock", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE)
        punk_genre = G(Criteria, name="Punk", user=self.test_user, type=CRITERIA_TYPES_ID.GENRE, parent=rock_genre)
        punk_playlist = punk_genre.criteria_playlist.playlist  # type: ignore
        punk_fr_genre = G(Criteria,
                          name="Punk FR",
                          user=self.test_user,
                          type=CRITERIA_TYPES_ID.GENRE,
                          parent=punk_genre)

        track_second_in_punk = G(LibraryTrack, user=self.test_user, genre=punk_genre, title="Punk song")
        G(LibraryTrack, user=self.test_user, genre=punk_fr_genre, title="punk fr song")

        data = {PUT_FIELD.PARENT: rock_genre.uuid}  # type: ignore
        response = self.put_genre(genre_uuid=punk_fr_genre.uuid, data_dict=data)  # type: ignore
        assert response.status_code == status.HTTP_200_OK  # type: ignore
        assert PlaylistLibTrackRelation.objects.get(playlist=punk_playlist,
                                                    library_track=track_second_in_punk).position == 1
