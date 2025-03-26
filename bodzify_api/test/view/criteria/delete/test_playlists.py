from rest_framework import status

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.criteria.genre.GenrePlaylist import GenrePlaylist
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_delete_then_criteria_playlist_deleted(self):
        criteria = self.model_fixture_factory.create_genre(name='criteria')

        response = self._delete_genre(uuid=criteria.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert GenrePlaylist.objects.filter(criteria=criteria).exists() == False

    def test_delete_with_children_then_parent_playlist_not_changed(self):
        genre_rock = self.model_fixture_factory.create_genre(name='rock')
        genre_punk = self.model_fixture_factory.create_genre(name='punk', parent=genre_rock)
        genre_punk_hardcore = self.model_fixture_factory.create_genre(name='punk hardcore', parent=genre_punk)

        lib_track_rock_added_first = self.model_fixture_factory.create_lib_track_with_file(
            title='rock first', genre=genre_rock, use_manager_for_genre_playlist_adding=True)
        lib_track_punk_added_second = self.model_fixture_factory.create_lib_track_with_file(
            title='punk second', genre=genre_punk, use_manager_for_genre_playlist_adding=True)
        lib_track_punk_hardcore_added_third = self.model_fixture_factory.create_lib_track_with_file(
            title='punk hardcore third', genre=genre_punk_hardcore, use_manager_for_genre_playlist_adding=True)
        lib_track_rock_added_fourth = self.model_fixture_factory.create_lib_track_with_file(
            title='rock fourth', genre=genre_rock, use_manager_for_genre_playlist_adding=True)
        lib_track_punk_hardcore_added_fifth = self.model_fixture_factory.create_lib_track_with_file(
            title='punk hardcore fifth', genre=genre_punk_hardcore, use_manager_for_genre_playlist_adding=True)
        lib_track_punk_added_sixth = self.model_fixture_factory.create_lib_track_with_file(
            title='punk sixth', genre=genre_punk, use_manager_for_genre_playlist_adding=True)

        rock_playlist: Playlist = Playlist.objects.get(user=self.test_user1, uuid=genre_rock.criteria_playlist.uuid)
        rock_tracks_dict_by_position = rock_playlist.lib_tracks_not_archived_dict_by_position
        assert len(rock_tracks_dict_by_position) == 6
        assert rock_tracks_dict_by_position[1].uuid == lib_track_punk_added_sixth.uuid
        assert rock_tracks_dict_by_position[2].uuid == lib_track_punk_hardcore_added_fifth.uuid
        assert rock_tracks_dict_by_position[3].uuid == lib_track_rock_added_fourth.uuid
        assert rock_tracks_dict_by_position[4].uuid == lib_track_punk_hardcore_added_third.uuid
        assert rock_tracks_dict_by_position[5].uuid == lib_track_punk_added_second.uuid
        assert rock_tracks_dict_by_position[6].uuid == lib_track_rock_added_first.uuid

        response = self._delete_genre(uuid=genre_punk.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        rock_playlist: Playlist = Playlist.objects.get(user=self.test_user1, uuid=genre_rock.criteria_playlist.uuid)
        rock_tracks_dict_by_position = rock_playlist.lib_tracks_not_archived_dict_by_position
        assert len(rock_tracks_dict_by_position) == 6
        assert rock_tracks_dict_by_position[1].uuid == lib_track_punk_added_sixth.uuid
        assert rock_tracks_dict_by_position[2].uuid == lib_track_punk_hardcore_added_fifth.uuid
        assert rock_tracks_dict_by_position[3].uuid == lib_track_rock_added_fourth.uuid
        assert rock_tracks_dict_by_position[4].uuid == lib_track_punk_hardcore_added_third.uuid
        assert rock_tracks_dict_by_position[5].uuid == lib_track_punk_added_second.uuid
        assert rock_tracks_dict_by_position[6].uuid == lib_track_rock_added_first.uuid

    def test_delete_root_criteria_with_children_then_direct_tracks_in_criterialess_playlist_in_first_positions(self):
        genreless_lib_track_added_first = self.model_fixture_factory.create_lib_track_with_file(
            title='genreless first', use_manager_for_genre_playlist_adding=True)
        genreless_lib_track_added_second = self.model_fixture_factory.create_lib_track_with_file(
            title='genreless second', use_manager_for_genre_playlist_adding=True)

        rock_criteria = self.model_fixture_factory.create_genre(name='rock')
        indie_criteria = self.model_fixture_factory.create_genre(name='indie', parent=rock_criteria)
        punk_criteria = self.model_fixture_factory.create_genre(name='punk', parent=rock_criteria)
        punk_hardcore_criteria = self.model_fixture_factory.create_genre(name='punk hardcore', parent=punk_criteria)

        rock_lib_track_added_third = self.model_fixture_factory.create_lib_track_with_file(
            title='rock third', genre=rock_criteria, use_manager_for_genre_playlist_adding=True)
        punk_lib_track_added_fourth = self.model_fixture_factory.create_lib_track_with_file(
            title='punk fourth', genre=punk_criteria, use_manager_for_genre_playlist_adding=True)
        punk_hardcore_lib_track_added_fifth = self.model_fixture_factory.create_lib_track_with_file(
            title='punk hardcore fifth', genre=punk_hardcore_criteria, use_manager_for_genre_playlist_adding=True)
        indie_lib_track_added_sixth = self.model_fixture_factory.create_lib_track_with_file(
            title='indie sixth', genre=indie_criteria, use_manager_for_genre_playlist_adding=True)
        punk_lib_track_added_seventh = self.model_fixture_factory.create_lib_track_with_file(
            title='punk seventh', genre=punk_criteria, use_manager_for_genre_playlist_adding=True)
        punk_hardcore_lib_track_added_eighth = self.model_fixture_factory.create_lib_track_with_file(
            title='punk hardcore eighth', genre=punk_hardcore_criteria, use_manager_for_genre_playlist_adding=True)
        indie_lib_track_added_ninth = self.model_fixture_factory.create_lib_track_with_file(
            title='indie ninth', genre=indie_criteria, use_manager_for_genre_playlist_adding=True)
        rock_lib_track_added_tenth = self.model_fixture_factory.create_lib_track_with_file(
            title='rock tenth', genre=rock_criteria, use_manager_for_genre_playlist_adding=True)

        response = self._delete_genre(uuid=rock_criteria.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        genreless_playlist: Playlist = GenrePlaylist.objects.get(user=self.test_user1, criteria=None)
        lib_tracks_dict_by_position = genreless_playlist.lib_tracks_not_archived_dict_by_position
        assert len(lib_tracks_dict_by_position) == 4
        assert lib_tracks_dict_by_position[1].uuid == rock_lib_track_added_tenth.uuid
        assert lib_tracks_dict_by_position[2].uuid == rock_lib_track_added_third.uuid
        assert lib_tracks_dict_by_position[3].uuid == genreless_lib_track_added_second.uuid
        assert lib_tracks_dict_by_position[4].uuid == genreless_lib_track_added_first.uuid

    def test_delete_root_criteria_with_archived_lib_tracks_then_not_archived_tracks_in_criterialess_playlist_in_first_positions_and_archived_ones_last(self):
        genreless_lib_track_added_first = self.model_fixture_factory.create_lib_track_with_file(
            title='genreless first', use_manager_for_genre_playlist_adding=True)
        genreless_lib_track_added_second = self.model_fixture_factory.create_lib_track_with_file(
            title='genreless second', use_manager_for_genre_playlist_adding=True)

        rock = self.model_fixture_factory.create_genre(name='rock')
        rock_not_archived_first = self.model_fixture_factory.create_lib_track_with_file(
            title='rock not archived first', genre=rock, use_manager_for_genre_playlist_adding=True)
        rock_not_archived_second = self.model_fixture_factory.create_lib_track_with_file(
            title='rock not archived second', genre=rock, use_manager_for_genre_playlist_adding=True)
        rock_archived_third = self.model_fixture_factory.create_lib_track_with_file(
            title='rock archived third', genre=rock, use_manager_for_genre_playlist_adding=True)

        response = self._put_lib_track(uuid=rock_archived_third.uuid, is_from_lib_track_test_case=False, archived=True)
        assert response.status_code == status.HTTP_200_OK

        rock_archived_fourth = self.model_fixture_factory.create_lib_track_with_file(
            title='rock archived fourth', genre=rock, use_manager_for_genre_playlist_adding=True)

        response = self._put_lib_track(uuid=rock_archived_fourth.uuid, is_from_lib_track_test_case=False, archived=True)
        assert response.status_code == status.HTTP_200_OK

        response = self._delete_genre(uuid=rock.uuid)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        genreless_playlist: Playlist = GenrePlaylist.objects.get(user=self.test_user1, criteria=None)
        lib_tracks_dict_by_position = genreless_playlist.lib_tracks_not_archived_dict_by_position
        assert len(lib_tracks_dict_by_position) == 6
        assert lib_tracks_dict_by_position[1].uuid == rock_not_archived_second.uuid
        assert lib_tracks_dict_by_position[2].uuid == rock_not_archived_first.uuid
        assert lib_tracks_dict_by_position[3].uuid == genreless_lib_track_added_second.uuid
        assert lib_tracks_dict_by_position[4].uuid == genreless_lib_track_added_first.uuid
        assert rock_archived_fourth.uuid in [lib_tracks_dict_by_position[5].uuid, lib_tracks_dict_by_position[6].uuid]
        assert rock_archived_third.uuid in [lib_tracks_dict_by_position[5].uuid, lib_tracks_dict_by_position[6].uuid]
