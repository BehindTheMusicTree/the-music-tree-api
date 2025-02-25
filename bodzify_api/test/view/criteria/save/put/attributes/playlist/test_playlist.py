from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import \
    CriteriaPlaylist
from bodzify_api.serializer.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_name(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_new_name = "Punk"

        response = self._put_genre(uuid=genre_rock.uuid, **{PutFields.NAME_PUBLIC: genre_new_name})

        assert response.status_code == status.HTTP_200_OK
        assert self.saved_object.name == genre_new_name

    def test_new_parent_then_update_playlist_parent(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        hardcore_genre = self.model_fixture_factory.create_genre(name="Hardcore")

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: hardcore_genre.uuid})

        assert response.status_code == status.HTTP_200_OK
        punk_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=genre_punk)
        hardcore_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=hardcore_genre)
        assert punk_playlist.parent == hardcore_playlist

    def test_new_root_then_update_playlist_root(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        hardcore_genre = self.model_fixture_factory.create_genre(name="Hardcore")

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: hardcore_genre.uuid})

        assert response.status_code == status.HTTP_200_OK
        punk_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=genre_punk)
        hardcore_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=hardcore_genre)
        assert punk_playlist.root == hardcore_playlist

    def test_new_parent_then_update_new_parent_playlist(self):
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        track = self.model_fixture_factory.create_lib_track_with_file(
            title="Punk song", genre=genre_punk,
            use_manager_for_genre_playlist_adding=True)
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_200_OK
        playlist_rock: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=genre_rock)
        assert playlist_rock.lib_tracks.first() == track

    def test_new_parent_not_acendant_of_old_parent_then_remove_criteria_playlist_tracks_from_old_criteria_ascendants_playlist(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        track = self.model_fixture_factory.create_lib_track_with_file(
            title="Rock song", genre=genre_punk,
            use_manager_for_genre_playlist_adding=True)

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: ''})

        assert response.status_code == status.HTTP_200_OK
        playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=genre_rock)
        assert playlist.lib_tracks.first() != track

    def test_new_parent_undirect_ascendant_of_old_parent_then_update_positions_in_criterias_in_between(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        punk_fr_genre = self.model_fixture_factory.create_genre(name="Punk FR", parent=genre_punk)
        track_punk = self.model_fixture_factory.create_lib_track_with_file(
            title="Punk song", genre=genre_punk,
            use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="punk fr song", genre=punk_fr_genre,
            use_manager_for_genre_playlist_adding=True)

        response = self._put_genre(uuid=punk_fr_genre.uuid, **{PutFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert genre_punk.criteria_playlist.lib_tracks.count() == 1
        assert genre_punk.criteria_playlist.lib_tracks.first() == track_punk
