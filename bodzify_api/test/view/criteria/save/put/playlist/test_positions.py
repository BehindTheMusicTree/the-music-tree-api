#!/usr/bin/env python

from rest_framework import status
from bodzify_api.model.PlaylistLibTrackRelation import PlaylistLibTrackRelation
from bodzify_api.model.criteria.CriteriaType import CriteriaTypesId
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.criteria.input.schema.endpoint.put import Fields as PUT_FIELD
from bodzify_api.test.view.criteria.CriteriaTestCase import CriteriaTestCase


class TestCase(CriteriaTestCase):

    def test_new_parent_then_tracks_in_same_order_and_added_at_the_beginning(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        rock_playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).base_playlist
        lib_track_previously_second_in_rock = self.model_fixture_factory.create_lib_track(genre=rock_genre, title="kok")
        lib_track_previously_first_in_rock = self.model_fixture_factory.create_lib_track(genre=rock_genre, title="lkdw")

        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        lib_track_previously_second_in_punk = self.model_fixture_factory.create_lib_track(
            genre=punk_genre, title="punk song")
        lib_track_previously_first_in_punk = self.model_fixture_factory.create_lib_track(genre=punk_genre, title="loul")

        data = {PUT_FIELD.PARENT: rock_genre.uuid}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        playlist_lib_track_relations = PlaylistLibTrackRelation.objects.filter(base_playlist=rock_playlist)
        assert playlist_lib_track_relations.get(library_track=lib_track_previously_first_in_punk).position == 1
        assert playlist_lib_track_relations.get(library_track=lib_track_previously_second_in_punk).position == 2
        assert playlist_lib_track_relations.get(library_track=lib_track_previously_first_in_rock).position == 3
        assert playlist_lib_track_relations.get(library_track=lib_track_previously_second_in_rock).position == 4

    def test_new_parent_then_tracks_in_same_order_and_added_at_the_beginning_of_parent_of_parent(self):
        guitare_genre = self.model_fixture_factory.create_genre(name="Guitare")
        guitare_playlist = CriteriaPlaylist.objects.get(criteria=guitare_genre).base_playlist
        lib_track_previously_second_in_guitare = self.model_fixture_factory.create_lib_track(
            genre=guitare_genre, title="guitare2")
        lib_track_previously_first_in_guitare = self.model_fixture_factory.create_lib_track(
            genre=guitare_genre, title="guitare1")

        rock_genre = self.model_fixture_factory.create_genre(name="Rock", parent=guitare_genre)
        lib_track_previously_second_in_rock = self.model_fixture_factory.create_lib_track(
            genre=rock_genre, title="rock2")
        lib_track_previously_first_in_rock = self.model_fixture_factory.create_lib_track(
            genre=rock_genre, title="rock1")

        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        lib_track_previously_second_in_punk = self.model_fixture_factory.create_lib_track(
            genre=punk_genre, title="punk2")
        lib_track_previously_first_in_punk = self.model_fixture_factory.create_lib_track(
            genre=punk_genre, title="punk1")

        data = {PUT_FIELD.PARENT: rock_genre.uuid}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        playlist_lib_track_relations = PlaylistLibTrackRelation.objects.filter(base_playlist=guitare_playlist)
        tracks_positions = {relation.library_track.uuid: relation.position for relation in playlist_lib_track_relations}
        assert tracks_positions[lib_track_previously_first_in_punk.uuid] == 1
        assert tracks_positions[lib_track_previously_second_in_punk.uuid] == 2
        assert tracks_positions[lib_track_previously_first_in_rock.uuid] == 3
        assert tracks_positions[lib_track_previously_second_in_rock.uuid] == 4
        assert tracks_positions[lib_track_previously_first_in_guitare.uuid] == 5
        assert tracks_positions[lib_track_previously_second_in_guitare.uuid] == 6

    def test_new_parent_not_acendant_of_old_parent_then_update_positions_in_old_parent(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        rock_playlist = CriteriaPlaylist.objects.get(criteria=rock_genre).base_playlist

        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)

        track_fourth_in_rock = self.model_fixture_factory.create_lib_track(genre=rock_genre, title="Rock song 2")
        self.model_fixture_factory.create_lib_track(genre=punk_genre, title="Punk song 2")
        track_second_in_rock = self.model_fixture_factory.create_lib_track(genre=rock_genre, title="Rock song")
        self.model_fixture_factory.create_lib_track(genre=punk_genre, title="Punk song")

        data = {PUT_FIELD.PARENT: ''}
        response = self.put_genre(genre_uuid=punk_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK

        playlist_lib_track_relations = PlaylistLibTrackRelation.objects.filter(base_playlist=rock_playlist)
        tracks_positions = {relation.library_track.uuid: relation.position for relation in playlist_lib_track_relations}
        assert tracks_positions[track_second_in_rock.uuid] == 1
        assert tracks_positions[track_fourth_in_rock.uuid] == 2

    def test_new_parent_undirect_ascendant_of_old_parent_then_update_positions_in_criterias_in_between(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punk_playlist = punk_genre.criteria_playlist.base_playlist  # type: ignore
        punk_fr_genre = self.model_fixture_factory.create_genre(name="Punk FR", parent=punk_genre)

        track_second_in_punk = self.model_fixture_factory.create_lib_track(genre=punk_genre, title="Punk song")
        self.model_fixture_factory.create_lib_track(genre=punk_fr_genre, title="punk fr song")

        data = {PUT_FIELD.PARENT: rock_genre.uuid}
        response = self.put_genre(genre_uuid=punk_fr_genre.uuid, data_dict=data)
        assert response.status_code == status.HTTP_200_OK
        assert PlaylistLibTrackRelation.objects.get(base_playlist=punk_playlist,
                                                    library_track=track_second_in_punk).position == 1
