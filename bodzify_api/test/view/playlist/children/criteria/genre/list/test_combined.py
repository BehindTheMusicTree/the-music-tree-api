from rest_framework import status
from datetime import timedelta
from django.utils import timezone

from bodzify_api.model.criteria.type.CriteriaTypePks import CriteriaTypePks
from bodzify_api.model.playlist.Fields import Fields
from bodzify_api.model.playlist.children.criteria.genre.GenrePlaylist import GenrePlaylist
from bodzify_api.serializer.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from bodzify_api.test.view.playlist.children.criteria.genre.GenrePlaylistTestCase import GenrePlaylistTestCase
from bodzify_api.filtering.set.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields


class TestCase(GenrePlaylistTestCase):

    def test_combined_then_ok(self):
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_punky = self.model_fixture_factory.create_genre(name="Punky", parent=genre_rock)

        response = self._list_genre_playlists(name='PU', parent=genre_rock.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert genre_punk.name in result_names
        assert genre_punky.name in result_names

    def test_name_parent_and_created_on_range_then_ok(self):
        now = timezone.now()
        past = now - timedelta(days=5)
        future = now + timedelta(days=5)

        genreless_playlist: GenrePlaylist = GenrePlaylist.objects.get(
            user=self.test_user1, type=CriteriaTypePks.GENRE, criteria=None)
        genreless_playlist.created_on = now
        genreless_playlist.save(update_fields=[Fields.CREATED_ON])

        # Create parent genre
        genre_rock = self.model_fixture_factory.create_genre(name="Rock")

        # Create child genres with different created_on dates
        genre_punk = self.model_fixture_factory.create_genre(name="Punk", parent=genre_rock)
        genre_punk.criteria_playlist.created_on = now
        genre_punk.criteria_playlist.save(update_fields=[Fields.CREATED_ON])

        genre_metal = self.model_fixture_factory.create_genre(name="Metal", parent=genre_rock)
        genre_metal.criteria_playlist.created_on = past
        genre_metal.criteria_playlist.save(update_fields=[Fields.CREATED_ON])

        genre_indie = self.model_fixture_factory.create_genre(name="Indie", parent=genre_rock)
        genre_indie.criteria_playlist.created_on = future
        genre_indie.criteria_playlist.save(update_fields=[Fields.CREATED_ON])

        # Create unrelated genre
        self.model_fixture_factory.create_genre(name="Pop", created_on=now)

        response = self._list_genre_playlists(
            name='e',  # matches "Metal" and "Indie" but not "Punk"
            parent=genre_rock.criteria_playlist.uuid,
            **{
                PrivateUniqueResourceFields.CREATED_ON_GTE: past.isoformat(),
                PrivateUniqueResourceFields.CREATED_ON_LTE: now.isoformat()
            }
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert genre_metal.name in result_names
        assert genre_indie.name not in result_names
        assert genre_punk.name not in result_names
