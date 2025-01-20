from rest_framework import status

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.criteria.input.put import Fields as PutFields
from bodzify_api.test.view.genre.GenreTestCase import GenreTestCase


class TestCase(GenreTestCase):

    def test_renaming(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        genre_new_name = "Punk"

        response = self._put_genre(uuid=rock_genre.uuid, **{PutFields.NAME: genre_new_name})

        assert response.status_code == status.HTTP_200_OK
        playlist = self.saved_genre
        assert playlist.name == genre_new_name

    def test_new_parent_then_update_playlist_parent(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        hardcore_genre = self.model_fixture_factory.create_genre(name="Hardcore")

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: hardcore_genre.uuid})

        assert response.status_code == status.HTTP_200_OK
        punk_playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=punk_genre)
        hardcore_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=hardcore_genre)
        assert punk_playlist.parent == hardcore_playlist

    def test_new_root_then_update_playlist_root(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        hardcore_genre = self.model_fixture_factory.create_genre(name="Hardcore")

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: hardcore_genre.uuid})

        assert response.status_code == status.HTTP_200_OK
        punk_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=punk_genre)
        hardcore_playlist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=hardcore_genre)
        assert punk_playlist.root == hardcore_playlist

    def test_new_parent_then_update_new_parent_playlist(self):
        genre_punk = self.model_fixture_factory.create_genre(name="Punk")
        track = self.model_fixture_factory.create_lib_track_with_file(genre=genre_punk, title="Rock song")
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        response = self._put_genre(uuid=genre_punk.uuid, **{PutFields.PARENT: genre_rock.uuid})

        assert response.status_code == status.HTTP_200_OK
        playlist_rock: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=genre_rock)
        assert playlist_rock.library_tracks.first() == track

    def test_new_parent_not_acendant_of_old_parent_then_remove_criteria_playlist_tracks_from_old_criteria_ascendants_playlist(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        track = self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre, title="Rock song")

        response = self._put_genre(uuid=punk_genre.uuid, **{PutFields.PARENT: ''})

        assert response.status_code == status.HTTP_200_OK
        playlist: CriteriaPlaylist = CriteriaPlaylist.objects.get(user=self.test_user1, criteria=rock_genre)
        assert playlist.library_tracks.first() != track

    def test_new_parent_undirect_ascendant_of_old_parent_then_update_positions_in_criterias_in_between(self):
        rock_genre = self.model_fixture_factory.create_genre(name="Rock")
        punk_genre = self.model_fixture_factory.create_genre(name="Punk", parent=rock_genre)
        punk_fr_genre = self.model_fixture_factory.create_genre(name="Punk FR", parent=punk_genre)
        track_punk = self.model_fixture_factory.create_lib_track_with_file(genre=punk_genre, title="Punk song")
        self.model_fixture_factory.create_lib_track_with_file(genre=punk_fr_genre, title="punk fr song")

        response = self._put_genre(uuid=punk_fr_genre.uuid, **{PutFields.PARENT: rock_genre.uuid})

        assert response.status_code == status.HTTP_200_OK
        assert punk_genre.criteria_playlist.library_tracks.count() == 1
        assert punk_genre.criteria_playlist.library_tracks.first() == track_punk
