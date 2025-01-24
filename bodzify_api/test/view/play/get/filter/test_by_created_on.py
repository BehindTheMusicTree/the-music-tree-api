from rest_framework import status

from bodzify_api.test.view.play.PlayTestCase import PlayTestCase
from bodzify_api.filtering.set.private_unique_resource.Fields import Fields


class TestCase(PlayTestCase):

    def test_filter_exact_match(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title='track')
        play = self.model_fixture_factory.create_play(content_object=track)
        created_on = play.created_on.isoformat()

        response = self._get_plays(**{Fields.CREATED_ON: created_on})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1

    def test_filter_greater_than(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title='track')
        old_play = self.model_fixture_factory.create_play(content_object=track)
        # Create a play 1 hour later
        new_play = self.model_fixture_factory.create_play(content_object=track)

        response = self._get_plays(**{f"{Fields.CREATED_ON}__gt": old_play.created_on.isoformat()})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1

    def test_filter_less_than(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title='track')
        old_play = self.model_fixture_factory.create_play(content_object=track)
        # Create a play 1 hour later
        new_play = self.model_fixture_factory.create_play(content_object=track)

        response = self._get_plays(**{f"{Fields.CREATED_ON}__lt": new_play.created_on.isoformat()})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1

    def test_filter_between_dates(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title='track')
        play1 = self.model_fixture_factory.create_play(content_object=track)
        play2 = self.model_fixture_factory.create_play(content_object=track)
        play3 = self.model_fixture_factory.create_play(content_object=track)

        # Get plays between first and last play
        response = self._get_plays(**{
            f"{Fields.CREATED_ON}__gt": play1.created_on.isoformat(),
            f"{Fields.CREATED_ON}__lt": play3.created_on.isoformat()
        })
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 1  # Should only return play2

    def test_invalid_date_format(self):
        track = self.model_fixture_factory.create_lib_track_with_file(title='track')
        self.model_fixture_factory.create_play(content_object=track)

        response = self._get_plays(**{Fields.CREATED_ON: 'invalid-date'})
        assert response.status_code == status.HTTP_200_OK
        assert self.results_overall_total == 0  # Invalid date should return no results
