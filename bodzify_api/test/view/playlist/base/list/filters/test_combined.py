from rest_framework import status
from datetime import timedelta
from django.utils import timezone

from bodzify_api.filtering.set.playlist.Fields import Fields as Filters
from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.children.criteria.CriterialessPlaylistNames import CriterialessPlaylistNames
from bodzify_api.model.playlist.PlaylistTypesLabel import PlaylistTypesLabel
from bodzify_api.model.playlist.children.criteria.tag.TagPlaylist import TagPlaylist
from bodzify_api.serializer.model.playlist.base.output.detailed import Fields as PlaylistGetFields
from bodzify_api.test.view.playlist.base.PlaylistTestCase import PlaylistTestCase
from bodzify_api.filtering.set.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields


class TestCase(PlaylistTestCase):

    def test_type_genre_and_name_tagless_then_no_result(self):
        data_dict = {
            Filters.TYPE_LABEL_PUBLIC: PlaylistTypesLabel.GENRE,
            Filters.NAME: CriterialessPlaylistNames.TAG
        }
        response = self._get_playlists(**data_dict)

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 0

    def test_type_genre_and_name_genreless_then_one_result(self):
        data_dict = {
            Filters.TYPE_LABEL_PUBLIC: PlaylistTypesLabel.GENRE,
            Filters.NAME: CriterialessPlaylistNames.GENRE
        }
        response = self._get_playlists(**data_dict)

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 1
        assert self.results[0][PlaylistGetFields.NAME] == CriterialessPlaylistNames.GENRE

    def test_type_genre_and_genre_name_then_results(self):
        genre1_name = "Rock"
        self.model_fixture_factory.create_genre(name=genre1_name)
        genre2_name = "Punk rock"
        self.model_fixture_factory.create_genre(name=genre2_name)

        data_dict = {
            Filters.TYPE_LABEL_PUBLIC: PlaylistTypesLabel.GENRE,
            Filters.NAME: 'rock'
        }
        response = self._get_playlists(**data_dict)

        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 2
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert genre1_name in names
        assert genre2_name in names

    def test_type_tag_and_created_on_range_then_results(self):
        """
        Test that we can filter playlists by type_label=TAG and created_on date range.
        The test creates three playlists:
        - tagless_playlist: created at 'now'
        - tag1 (Summer): created at 'now'
        - tag2 (Winter): created at 'past'
        - tag3 (Spring): created at 'future'

        Then filters for all playlists of type TAG with created_on between past and now.
        """
        # Helper function to update playlist creation date and force sync to database
        def update_creation_date(playlist, date):
            # Apply date to the base playlist first
            playlist.created_on = date
            playlist.save(update_fields=['created_on'])

            # If it's a criteria playlist, also update the base Playlist entry
            # This ensures both inheritance model entries have same dates
            if hasattr(playlist, 'playlist_ptr'):
                playlist.playlist_ptr.created_on = date
                playlist.playlist_ptr.save(update_fields=['created_on'])

            print(f"Set {playlist.name} created_on to {date.isoformat()}")

        # Setup test timestamps
        now = timezone.now()
        past = now - timedelta(days=5)
        future = now + timedelta(days=5)

        print(f"\n===== TAG AND DATE RANGE TEST =====")
        print(f"Time values: past={past.isoformat()}, now={now.isoformat()}, future={future.isoformat()}")

        # Get the tagless playlist
        tagless_playlist = TagPlaylist.objects.get(
            user=self.test_user1, type=CriteriaTypePks.TAG, criteria=None)
        update_creation_date(tagless_playlist, now)

        # Create test tags with different creation dates
        tag1_name = "Summer"
        tag1 = self.model_fixture_factory.create_tag(name=tag1_name)
        update_creation_date(tag1, now)
        update_creation_date(tag1.criteria_playlist, now)

        tag2_name = "Winter"
        tag2 = self.model_fixture_factory.create_tag(name=tag2_name)
        update_creation_date(tag2, past)
        update_creation_date(tag2.criteria_playlist, past)

        tag3_name = "Spring"
        tag3 = self.model_fixture_factory.create_tag(name=tag3_name)
        update_creation_date(tag3, future)
        update_creation_date(tag3.criteria_playlist, future)

        # Verify all playlists are properly set in database
        print("\nVerifying all tag playlists in database:")
        for playlist in TagPlaylist.objects.filter(user=self.test_user1):
            print(f"  {playlist.name}: created_on={playlist.created_on.isoformat()}")

        # Test with date range filter
        data_dict = {
            Filters.TYPE_LABEL_PUBLIC: PlaylistTypesLabel.TAG,
            PrivateUniqueResourceFields.CREATED_ON_GTE: past.isoformat(),
            PrivateUniqueResourceFields.CREATED_ON_LTE: now.isoformat()
        }

        print(f"\nApplying filter: {data_dict}")
        response = self._get_playlists(**data_dict)

        print(f"Response status: {response.status_code}")
        print(f"Results count: {len(self.results)}")
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        print(f"Names in results: {names}")

        # Make assertions for the test
        assert response.status_code == status.HTTP_200_OK
        assert len(self.results) == 3
        names = [result[PlaylistGetFields.NAME] for result in self.results]
        assert tag1_name in names, f"Tag1 '{tag1_name}' should be in results"
        assert tag2_name in names, f"Tag2 '{tag2_name}' should be in results"
        assert tagless_playlist.name in names, f"Tagless playlist '{tagless_playlist.name}' should be in results"
        assert tag3_name not in names, f"Tag3 '{tag3_name}' should NOT be in results"
