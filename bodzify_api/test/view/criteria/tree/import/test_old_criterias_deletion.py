from rest_framework import status

from bodzify_api.model.criteria.children.genre.Genre import Genre
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.model.playlist.children.criteria.genre.GenrePlaylist import GenrePlaylist
from bodzify_api.model.track.lib.LibraryTrack import LibraryTrack
from bodzify_api.test.view.criteria.GenreTestCase import GenreTestCase


class TestOldCriteriasDeletion(GenreTestCase):
    def test_old_genre_is_deleted(self):
        old_genre = self.model_fixture_factory.create_genre(name="Old Rock")
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 1", use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 2", use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 3", use_manager_for_genre_playlist_adding=True)

        # Import new tree
        tree_data = [{"name": "New Rock", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert not Genre.objects.filter(uuid=old_genre.uuid).exists()

    def test_old_playlist_is_deleted(self):
        old_genre = self.model_fixture_factory.create_genre(name="Old Rock")
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 1", use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 2", use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 3", use_manager_for_genre_playlist_adding=True)

        # Import new tree
        tree_data = [{"name": "New Rock", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert not Playlist.objects.filter(uuid=old_genre.criteria_playlist.uuid).exists()

    def test_tracks_are_moved_to_criterialess_playlist(self):
        # Create initial genre with tracks
        self.model_fixture_factory.create_genre(name="Old Rock")
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 1", use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 2", use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 3", use_manager_for_genre_playlist_adding=True)

        # Import new tree
        tree_data = [{"name": "New Rock", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED

        # Verify tracks are moved to criterialess playlist
        criterialess_playlist = GenrePlaylist.objects.get(user=self.test_user1, criteria=None)
        tracks = LibraryTrack.objects.filter(playlist=criterialess_playlist)
        assert tracks.count() == 3
        track_titles = [track.title for track in tracks]
        assert "Track 1" in track_titles
        assert "Track 2" in track_titles
        assert "Track 3" in track_titles

    def test_genre_metadata_is_cleared(self):
        # Create initial genre with tracks
        self.model_fixture_factory.create_genre(name="Old Rock")
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 1", use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 2", use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 3", use_manager_for_genre_playlist_adding=True)

        # Import new tree
        tree_data = [{"name": "New Rock", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED

        # Verify genre metadata is cleared
        criterialess_playlist = GenrePlaylist.objects.get(user=self.test_user1, criteria=None)
        tracks = LibraryTrack.objects.filter(playlist=criterialess_playlist)
        for track in tracks:
            assert track.genre is None

    def test_new_genre_is_created(self):
        # Create initial genre with tracks
        self.model_fixture_factory.create_genre(name="Old Rock")
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 1", use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 2", use_manager_for_genre_playlist_adding=True)
        self.model_fixture_factory.create_lib_track_with_file(
            title="Track 3", use_manager_for_genre_playlist_adding=True)

        # Import new tree
        tree_data = [{"name": "New Rock", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED

        # Verify new genre exists
        new_genre = Genre.objects.get(name="New Rock")
        assert new_genre is not None
        assert new_genre.parent is None

    def test_multiple_old_criterias_deletion(self):
        # Create multiple genres with tracks
        old_genre1 = self.model_fixture_factory.create_genre(name="Old Rock 1")
        old_genre2 = self.model_fixture_factory.create_genre(name="Old Rock 2")

        track1 = self.model_fixture_factory.create_lib_track_with_file(
            title="Track 1", use_manager_for_genre_playlist_adding=True)
        track2 = self.model_fixture_factory.create_lib_track_with_file(
            title="Track 2", use_manager_for_genre_playlist_adding=True)

        # Import new tree
        tree_data = [{"name": "New Rock", "children": []}]
        response = self._post_genres_tree_import(tree_data)

        assert response.status_code == status.HTTP_201_CREATED

        # Verify all old genres are deleted
        assert not Genre.objects.filter(uuid__in=[old_genre1.uuid, old_genre2.uuid]).exists()

        # Verify all old playlists are deleted
        assert not Playlist.objects.filter(
            uuid__in=[old_genre1.criteria_playlist.uuid, old_genre2.criteria_playlist.uuid]).exists()

        # Verify all tracks are moved to criterialess playlist
        criterialess_playlist = GenrePlaylist.objects.get(user=self.test_user1, criteria=None)
        tracks = LibraryTrack.objects.filter(playlist=criterialess_playlist)
        assert tracks.count() == 2
        track_titles = [track.title for track in tracks]
        assert "Track 1" in track_titles
        assert "Track 2" in track_titles

        # Verify genre metadata is cleared for all tracks
        for track in tracks:
            assert track.genre is None

        # Verify new genre exists
        new_genre = Genre.objects.get(name="New Rock")
        assert new_genre is not None
        assert new_genre.parent is None
