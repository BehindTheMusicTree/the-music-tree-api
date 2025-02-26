
from datetime import timedelta

from django.utils import timezone
from django_filters import FilterSet

from bodzify_api.filtering.set.album.AlbumFilterSet import AlbumFilterSet
from bodzify_api.filtering.set.artist.ArtistFilterSet import ArtistFilterSet
from bodzify_api.filtering.set.criteria.CriteriaFilterSet import CriteriaFilterSet
from bodzify_api.filtering.set.lib_track.LibTrackFilterSet import LibTrackFilterSet
from bodzify_api.filtering.set.playlist.PlaylistFilterSet import PlaylistFilterSet
from bodzify_api.filtering.set.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields
from bodzify_api.filtering.set.search.SearchFilterSet import SearchFilterSet
from bodzify_api.test.ApiTestCase import ApiTestCase


class TestFilterInheritance(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.expected_filters = {
            PrivateUniqueResourceFields.CREATED_ON,
            PrivateUniqueResourceFields.CREATED_ON_GT,
            PrivateUniqueResourceFields.CREATED_ON_LT,
            PrivateUniqueResourceFields.CREATED_ON_GTE,
            PrivateUniqueResourceFields.CREATED_ON_LTE,
            PrivateUniqueResourceFields.UPDATED_ON,
            PrivateUniqueResourceFields.UPDATED_ON_GT,
            PrivateUniqueResourceFields.UPDATED_ON_LT,
            PrivateUniqueResourceFields.UPDATED_ON_GTE,
            PrivateUniqueResourceFields.UPDATED_ON_LTE
        }

    def assert_datetime_inherited_filters(self, filterset_class):
        filterset: FilterSet = filterset_class(queryset=filterset_class.Meta.model.objects.all())
        available_filters = set(filterset.filters.keys())
        inherited_filters = self.expected_filters & available_filters
        assert inherited_filters == self.expected_filters, \
            f"{filterset_class.__name__} is missing some datetime filters. " \
            f"Missing: {self.expected_filters - inherited_filters}"

        for filter_name in self.expected_filters:
            assert filter_name in filterset.filters, \
                f"{filterset_class.__name__} is missing filter: {filter_name}"
            assert hasattr(filterset.filters[filter_name], 'filter'), \
                f"{filterset_class.__name__}'s {filter_name} filter is not callable"

    def test_album_filter_inheritance(self):
        self.assert_datetime_inherited_filters(AlbumFilterSet)

    def test_search_param_filter_inheritance(self):
        self.assert_datetime_inherited_filters(SearchFilterSet)

    def test_artist_filter_inheritance(self):
        self.assert_datetime_inherited_filters(ArtistFilterSet)

    def test_lib_track_filter_inheritance(self):
        self.assert_datetime_inherited_filters(LibTrackFilterSet)

    def test_criteria_filter_inheritance(self):
        self.assert_datetime_inherited_filters(CriteriaFilterSet)

    def test_playlist_param_filter_inheritance(self):
        self.assert_datetime_inherited_filters(PlaylistFilterSet)

    def test_filter_functionality_using_a_concrete_model(self):
        now = timezone.now()

        past = now - timedelta(days=5)
        future = now + timedelta(days=5)

        past_record = self.model_fixture_factory.create_genre(name="Past Criteria", created_on=past, updated_on=past)
        present_record = self.model_fixture_factory.create_genre(name="Present Criteria",
                                                                 created_on=now,
                                                                 updated_on=now)

        future_record = self.model_fixture_factory.create_genre(name="Future Criteria",
                                                                created_on=future,
                                                                updated_on=future)

        filterset = CriteriaFilterSet({PrivateUniqueResourceFields.CREATED_ON: now.isoformat()},
                                      queryset=CriteriaFilterSet.Meta.model.objects.all())

        assert list(filterset.qs) == [present_record]

        filterset = CriteriaFilterSet({PrivateUniqueResourceFields.CREATED_ON_GT: now.isoformat()},
                                      queryset=CriteriaFilterSet.Meta.model.objects.all())

        assert list(filterset.qs) == [future_record]

        filterset = CriteriaFilterSet({PrivateUniqueResourceFields.CREATED_ON_LT: now.isoformat()},
                                      queryset=CriteriaFilterSet.Meta.model.objects.all())

        assert list(filterset.qs) == [past_record]

        filterset = CriteriaFilterSet({PrivateUniqueResourceFields.CREATED_ON_GTE: past.isoformat(),
                                       PrivateUniqueResourceFields.CREATED_ON_LTE: now.isoformat()},
                                      queryset=CriteriaFilterSet.Meta.model.objects.all())

        assert set(filterset.qs) == {past_record, present_record}
