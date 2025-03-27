from rest_framework import status
from datetime import timedelta
from django.utils import timezone

from bodzify_api.serializer.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from bodzify_api.test.view.playlist.children.criteria.tag.TagPlaylistTestCase import TagPlaylistTestCase
from bodzify_api.filtering.set.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields


class TestCase(TagPlaylistTestCase):

    def test_combined_then_ok(self):
        tag_fiesta = self.model_fixture_factory.create_tag(name="Fiesta")
        tag_punk = self.model_fixture_factory.create_tag(name="Punk", parent=tag_fiesta)
        tag_punky = self.model_fixture_factory.create_tag(name="Punky", parent=tag_fiesta)

        response = self._get_tag_playlists(name='PU', parent=tag_fiesta.criteria_playlist.uuid)

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 2
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert tag_punk.name in result_names
        assert tag_punky.name in result_names

    def test_name_parent_and_updated_on_range_then_ok(self):
        now = timezone.now()
        past = now - timedelta(days=5)
        future = now + timedelta(days=5)

        # Create parent tag
        tag_fiesta = self.model_fixture_factory.create_tag(name="Fiesta")

        # Create child tags with different updated_on dates
        tag_summer = self.model_fixture_factory.create_tag(name="Summer", parent=tag_fiesta)
        tag_summer.criteria_playlist.updated_on = now
        tag_summer.criteria_playlist.save()

        tag_winter = self.model_fixture_factory.create_tag(name="Winter", parent=tag_fiesta)
        tag_winter.criteria_playlist.updated_on = past
        tag_winter.criteria_playlist.save()

        tag_spring = self.model_fixture_factory.create_tag(name="Spring", parent=tag_fiesta)
        tag_spring.criteria_playlist.updated_on = future
        tag_spring.criteria_playlist.save()

        # Create unrelated tag
        self.model_fixture_factory.create_tag(name="Beach", updated_on=now)

        response = self._get_tag_playlists(
            name='s',  # matches "Summer" and "Spring" but not "Winter"
            parent=tag_fiesta.criteria_playlist.uuid,
            **{
                PrivateUniqueResourceFields.UPDATED_ON_GTE: past.isoformat(),
                PrivateUniqueResourceFields.UPDATED_ON_LTE: now.isoformat()
            }
        )

        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1
        result_names = [result[RietrieveFields.NAME] for result in self.results]
        assert tag_summer.name in result_names
        assert tag_spring.name not in result_names
        assert tag_winter.name not in result_names
