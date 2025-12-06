from rest_framework import status
from datetime import timedelta
from django.utils import timezone

from bodzify_api.model.playlist.children.criteria.tag.TagPlaylist import TagPlaylist
from bodzify_api.serializer.model.playlist.children.criteria.output.detailed import Fields as RietrieveFields
from bodzify_api.test.integration.view.playlist.children.criteria.tag.TagPlaylistTestCase import TagPlaylistTestCase
from bodzify_api.model.playlist.children.criteria.Fields import Fields as ModelFields
from bodzify_api.filtering.set.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields
from bodzify_api.filtering.set.playlist.children.criteria.Fields import Fields as CriteriaPlaylistFields


class TestCase(TagPlaylistTestCase):

    def test_combined_then_ok(self):
        tag_fiesta = self.model_fixture_factory.create_tag(name="Fiesta")
        tag_punk = self.model_fixture_factory.create_tag(name="Punk", parent=tag_fiesta)
        tag_punky = self.model_fixture_factory.create_tag(name="Punky", parent=tag_fiesta)

        filters = {'name': 'PU', 'parent': tag_fiesta.criteria_playlist.uuid}

        response = self._list_tag_playlists(**filters)

        assert response.status_code == status.HTTP_200_OK
        result_names = [result[RietrieveFields.NAME] for result in self.results]

        assert self.results_overall_total == 2
        assert tag_punk.name in result_names
        assert tag_punky.name in result_names

    def test_name_parent_and_updated_on_range_then_ok(self):
        now = timezone.now()
        past = now - timedelta(days=5)
        future = now + timedelta(days=2)

        tagless_playlist = TagPlaylist.objects.get(user=self.test_user1, criteria=None)
        tagless_playlist.updated_on = now
        tagless_playlist.save(update_fields=[ModelFields.UPDATED_ON])

        tag_fiesta = self.model_fixture_factory.create_tag(name="Fiesta")

        tag_summer = self.model_fixture_factory.create_tag(name="Summer", parent=tag_fiesta)
        tag_summer.criteria_playlist.updated_on = now
        tag_summer.criteria_playlist.save(update_fields=[ModelFields.UPDATED_ON])

        tag_winter = self.model_fixture_factory.create_tag(name="Winter", parent=tag_fiesta)
        tag_winter.criteria_playlist.updated_on = past
        tag_winter.criteria_playlist.save(update_fields=[ModelFields.UPDATED_ON])

        tag_spring = self.model_fixture_factory.create_tag(name="Spring", parent=tag_fiesta)

        # Create unrelated tag
        beach_tag = self.model_fixture_factory.create_tag(name="Beach", updated_on=now)

        filters = {
            CriteriaPlaylistFields.NAME_PUBLIC: 's',
            CriteriaPlaylistFields.PARENT: tag_fiesta.criteria_playlist.uuid,
            PrivateUniqueResourceFields.UPDATED_ON_GTE: past.isoformat(),
            PrivateUniqueResourceFields.UPDATED_ON_LTE: future.isoformat()  # Use buffer here
        }
        response = self._list_tag_playlists(**filters)

        assert response.status_code == status.HTTP_200_OK
        result_names = [result[RietrieveFields.NAME] for result in self.results]

        assert self.results_overall_total == 2

        assert tag_summer.name in result_names
        assert tag_winter.name not in result_names
