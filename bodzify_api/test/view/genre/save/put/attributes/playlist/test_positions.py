from rest_framework import status

from bodzify_api.model.lib_track_playlist_rel.LibTrackPlaylistRel import LibTrackPlaylistRel
from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_new_parent_then_tracks_in_same_order_and_added_at_the_beginning(self) -> None:
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        rock_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=rock_genre)
        lib_track_previously_second_in_rock = self.model_fixture_factory.create_lib_track_with_file(genre=rock_genre,
                                                                                                    title="kok")
        lib_track_previously_first_in_rock = self.model_fixture_factory.create_lib_track_with_file(genre=rock_genre,
                                                                                                   title="lkdw")

        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        lib_track_previously_second_in_punk = self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre,
                                                                                                    title="punk song")
        lib_track_previously_first_in_punk = self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre,
                                                                                                   title="loul")

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: rock_genre.uuid})
        assert response.status_code == status.HTTP_200_OK

        lib_track_playlist_rels = \
            LibTrackPlaylistRel.objects.filter(user=self.test_user2, playlist=rock_playlist)
        lib_track_playlist_rel: LibTrackPlaylistRel = lib_track_playlist_rels.get(
            library_track=lib_track_previously_first_in_punk)
        assert lib_track_playlist_rel.position == 1

        lib_track_playlist_rel = lib_track_playlist_rels.get(library_track=lib_track_previously_second_in_punk)
        assert lib_track_playlist_rel.position == 2

        lib_track_playlist_rel = lib_track_playlist_rels.get(library_track=lib_track_previously_first_in_rock)
        assert lib_track_playlist_rel.position == 3

        lib_track_playlist_rel = lib_track_playlist_rels.get(library_track=lib_track_previously_second_in_rock)
        assert lib_track_playlist_rel.position == 4

    def test_new_parent_then_tracks_in_same_order_and_added_at_the_beginning_of_parent_of_parent(self) -> None:
        guitare_genre = self.model_fixture_factory.create_genre(name="Guitare")
        guitare_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=guitare_genre)
        lib_track_previously_second_in_guitare = self.model_fixture_factory.create_lib_track_with_file(
            genre=guitare_genre, title="guitare2")
        lib_track_previously_first_in_guitare = self.model_fixture_factory.create_lib_track_with_file(
            genre=guitare_genre, title="guitare1")

        rock_genre = self.model_fixture_factory.create_genre(name="Rock", parent=guitare_genre)
        lib_track_previously_second_in_rock = self.model_fixture_factory.create_lib_track_with_file(genre=rock_genre,
                                                                                                    title="rock2")
        lib_track_previously_first_in_rock = self.model_fixture_factory.create_lib_track_with_file(genre=rock_genre,
                                                                                                   title="rock1")

        punk_genre = self.model_fixture_factory.create_genre(name="Punk")
        lib_track_previously_second_in_punk = self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre,
                                                                                                    title="punk2")
        lib_track_previously_first_in_punk = self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre,
                                                                                                   title="punk1")

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: rock_genre.uuid})

        assert response.status_code == status.HTTP_200_OK

        lib_track_playlist_rels: list[LibTrackPlaylistRel] = \
            list(LibTrackPlaylistRel.objects.filter(user=self.test_user2, playlist=guitare_playlist))
        tracks_positions = {relation.library_track.uuid: relation.position for relation in lib_track_playlist_rels}
        assert tracks_positions[lib_track_previously_first_in_punk.uuid] == 1
        assert tracks_positions[lib_track_previously_second_in_punk.uuid] == 2
        assert tracks_positions[lib_track_previously_first_in_rock.uuid] == 3
        assert tracks_positions[lib_track_previously_second_in_rock.uuid] == 4
        assert tracks_positions[lib_track_previously_first_in_guitare.uuid] == 5
        assert tracks_positions[lib_track_previously_second_in_guitare.uuid] == 6

    def test_new_parent_not_acendant_of_old_parent_then_update_positions_in_old_parent(self) -> None:
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        track_fourth_in_rock = self.model_fixture_factory.create_lib_track_with_file(genre=rock_genre,
                                                                                     title="Rock song 2")
        self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre, title="Punk song 2")
        track_second_in_rock = self.model_fixture_factory.create_lib_track_with_file(genre=rock_genre,
                                                                                     title="Rock song")
        self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre, title="Punk song")

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: ''})

        assert response.status_code == status.HTTP_200_OK
        lib_track_playlist_rels: list[LibTrackPlaylistRel] = \
            list(LibTrackPlaylistRel.objects.filter(user=self.test_user2, playlist=rock_genre.criteria_playlist))
        tracks_positions = {relation.library_track.uuid: relation.position for relation in lib_track_playlist_rels}
        assert tracks_positions[track_second_in_rock.uuid] == 1
        assert tracks_positions[track_fourth_in_rock.uuid] == 2

    def test_new_parent_undirect_ascendant_of_old_parent_then_update_positions_in_criterias_in_between(self) -> None:
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punk_fr_genre = self.model_fixture_factory.create_genre(name="Punk FR", parent=punk_genre)

        track_second_in_punk = self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre,
                                                                                     title="Punk song")
        self.model_fixture_factory.create_lib_track_with_file(genre=punk_fr_genre, title="punk fr song")

        response = self._put_genre(uuid=punk_fr_genre.uuid, **{PutFields.PARENT: rock_genre.uuid})

        assert response.status_code == status.HTTP_200_OK
        lib_track_playlist_rel: LibTrackPlaylistRel = \
            LibTrackPlaylistRel.objects.get(user=self.test_user2,
                                            playlist=punk_genre.criteria_playlist,
                                            library_track=track_second_in_punk)
        assert lib_track_playlist_rel.position == 1
