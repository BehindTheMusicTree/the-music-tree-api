from rest_framework import status

from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_new_parent_then_tracks_in_same_order_and_added_at_the_beginning(self) -> None:
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        rock_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=genre_rock)
        lib_track_previously_second_in_rock = self.model_fixture_factory.create_lib_track_with_file(
            title="kok", genre=genre_rock, use_manager_for_genre_playlist_adding=True)
        lib_track_previously_first_in_rock = self.model_fixture_factory.create_lib_track_with_file(
            title="lkdw", genre=genre_rock, use_manager_for_genre_playlist_adding=True)

        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        lib_track_previously_second_in_punk = self.model_fixture_factory.create_lib_track_with_file(
            title="punk song", genre=genre_punk, use_manager_for_genre_playlist_adding=True)
        lib_track_previously_first_in_punk = self.model_fixture_factory.create_lib_track_with_file(
            title="loul", genre=genre_punk, use_manager_for_genre_playlist_adding=True)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})
        assert response.status_code == status.HTTP_200_OK

        lib_track_playlist_rels = \
            LibTrackPlaylistRel.objects.filter(user=self.test_user1, playlist=rock_playlist)
        lib_track_playlist_rel: LibTrackPlaylistRel = lib_track_playlist_rels.get(
            lib_track=lib_track_previously_first_in_punk)
        assert lib_track_playlist_rel.position == 1

        lib_track_playlist_rel = lib_track_playlist_rels.get(lib_track=lib_track_previously_second_in_punk)
        assert lib_track_playlist_rel.position == 2

        lib_track_playlist_rel = lib_track_playlist_rels.get(lib_track=lib_track_previously_first_in_rock)
        assert lib_track_playlist_rel.position == 3

        lib_track_playlist_rel = lib_track_playlist_rels.get(lib_track=lib_track_previously_second_in_rock)
        assert lib_track_playlist_rel.position == 4

    def test_new_parent_then_tracks_in_same_order_and_added_at_the_beginning_of_parent_of_parent(self) -> None:
        genre_guitare = self.model_fixture_factory.create_genre(name="Guitare")
        lib_track_previously_second_in_guitare = self.model_fixture_factory.create_lib_track_with_file(
            title="guitare2", genre=genre_guitare, use_manager_for_genre_playlist_adding=True)
        lib_track_previously_first_in_guitare = self.model_fixture_factory.create_lib_track_with_file(
            title="guitare1", genre=genre_guitare, use_manager_for_genre_playlist_adding=True)

        assert genre_guitare.criteria_playlist.lib_tracks.count() == 2
        assert genre_guitare.criteria_playlist.lib_track_playlist_rels.get(
            lib_track=lib_track_previously_first_in_guitare).position == 1
        assert genre_guitare.criteria_playlist.lib_track_playlist_rels.get(
            lib_track=lib_track_previously_second_in_guitare).position == 2

        genre_rock = self.model_fixture_factory.create_genre(name="Rock", parent=genre_guitare)

        lib_track_previously_second_in_rock = self.model_fixture_factory.create_lib_track_with_file(
            title="rock2",
            genre=genre_rock,
            use_manager_for_genre_playlist_adding=True)
        lib_track_previously_first_in_rock = self.model_fixture_factory.create_lib_track_with_file(
            title="rock1",
            genre=genre_rock,
            use_manager_for_genre_playlist_adding=True)

        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        lib_track_previously_second_in_punk = self.model_fixture_factory.create_lib_track_with_file(
            title="punk2",
            genre=genre_punk,
            use_manager_for_genre_playlist_adding=True)
        lib_track_previously_first_in_punk = self.model_fixture_factory.create_lib_track_with_file(
            title="punk1",
            genre=genre_punk,
            use_manager_for_genre_playlist_adding=True)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})
        assert response.status_code == status.HTTP_200_OK
        lib_track_playlist_rels: list[LibTrackPlaylistRel] = \
            list(LibTrackPlaylistRel.objects.filter(user=self.test_user1, playlist=genre_guitare.criteria_playlist))
        tracks_uuids_positions = {
            relation.lib_track.uuid: relation.position for relation in lib_track_playlist_rels}
        assert tracks_uuids_positions[lib_track_previously_first_in_punk.uuid] == 1
        assert tracks_uuids_positions[lib_track_previously_second_in_punk.uuid] == 2
        assert tracks_uuids_positions[lib_track_previously_first_in_rock.uuid] == 3
        assert tracks_uuids_positions[lib_track_previously_second_in_rock.uuid] == 4
        assert tracks_uuids_positions[lib_track_previously_first_in_guitare.uuid] == 5
        assert tracks_uuids_positions[lib_track_previously_second_in_guitare.uuid] == 6

    def test_new_parent_not_acendant_of_old_parent_then_update_positions_in_old_parent(self) -> None:
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        track_fourth_in_rock = self.model_fixture_factory.create_lib_track_with_file(
            title="Rock song 2", genre=genre_rock, use_manager_for_genre_playlist_adding=True)
        track_third_in_rock = self.model_fixture_factory.create_lib_track_with_file(
            title="Punk song 2", genre=genre_punk, use_manager_for_genre_playlist_adding=True)
        track_second_in_rock = self.model_fixture_factory.create_lib_track_with_file(
            title="Rock song 1", genre=genre_rock, use_manager_for_genre_playlist_adding=True)
        track_first_in_rock = self.model_fixture_factory.create_lib_track_with_file(
            title="Punk song 1", genre=genre_punk, use_manager_for_genre_playlist_adding=True)
        assert track_fourth_in_rock.lib_track_playlist_rels.get(playlist=genre_rock.criteria_playlist).position == 4
        assert track_third_in_rock.lib_track_playlist_rels.get(playlist=genre_rock.criteria_playlist).position == 3
        assert track_second_in_rock.lib_track_playlist_rels.get(playlist=genre_rock.criteria_playlist).position == 2
        assert track_first_in_rock.lib_track_playlist_rels.get(playlist=genre_rock.criteria_playlist).position == 1

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: ''})

        assert response.status_code == status.HTTP_200_OK
        lib_track_playlist_rels: list[LibTrackPlaylistRel] = \
            list(LibTrackPlaylistRel.objects.filter(user=self.test_user1, playlist=genre_rock.criteria_playlist))
        assert len(lib_track_playlist_rels) == 2
        tracks_positions = {relation.lib_track.uuid: relation.position for relation in lib_track_playlist_rels}
        assert tracks_positions[track_second_in_rock.uuid] == 1
        assert tracks_positions[track_fourth_in_rock.uuid] == 2

    def test_new_parent_undirect_ascendant_of_old_parent_then_update_positions_in_criterias_in_between(self) -> None:
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        punk_fr_genre = self.model_fixture_factory.create_genre(name="Punk FR", parent=genre_punk)

        track_second_in_punk = self.model_fixture_factory.create_lib_track_with_file(
            title="Punk song", genre=genre_punk, use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="punk fr song", genre=punk_fr_genre, use_manager_for_genre_playlist_adding=True)

        response = self._put_genre(uuid=punk_fr_genre.uuid, **{PutFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_200_OK
        lib_track_playlist_rel: LibTrackPlaylistRel = \
            LibTrackPlaylistRel.objects.get(user=self.test_user1,
                                            playlist=genre_punk.criteria_playlist,
                                            lib_track=track_second_in_punk)
        assert lib_track_playlist_rel.position == 1
