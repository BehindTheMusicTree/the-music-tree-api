
from datetime import timedelta
from django.utils import timezone
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.filtering.set.private_unique_resource.PrivateUniqueResourceFilterSet \
    import PrivateUniqueResourceFilterSet
from bodzify_api.filtering.set.private_unique_resource.Fields import Fields as PrivateUniqueResourceFields
from bodzify_api.test.ApiTestCase import ApiTestCase


class TestPrivateUniqueResourceFilterSet(ApiTestCase):
    def setUp(self):
        super().setUp()
        self.now = timezone.now()
        self.past = self.now - timedelta(days=5)
        self.future = self.now + timedelta(days=5)

        self.past_record = self.model_fixture_factory.create_genre(name='rock',
                                                                   created_on=self.past,
                                                                   updated_on=self.past)

        self.present_record = self.model_fixture_factory.create_genre(name='pop',
                                                                      created_on=self.now,
                                                                      updated_on=self.now)
        self.future_record = self.model_fixture_factory.create_genre(name='jazz',
                                                                     created_on=self.future,
                                                                     updated_on=self.future)

    def test_created_on_exact_filter(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.CREATED_ON: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        assert list(filterset.qs) == [self.present_record]

    def test_created_on_gt_filter(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.CREATED_ON_GT: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        assert list(filterset.qs) == [self.future_record]

    def test_created_on_lt_filter(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.CREATED_ON_LT: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        assert list(filterset.qs) == [self.past_record]

    def test_created_on_gte_filter(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.CREATED_ON_GTE: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        assert set(filterset.qs) == {self.present_record, self.future_record}

    def test_created_on_lte_filter(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.CREATED_ON_LTE: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        assert set(filterset.qs) == {self.past_record, self.present_record}

    def test_updated_on_exact_filter(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.UPDATED_ON: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        assert list(filterset.qs) == [self.present_record]

    def test_updated_on_gt_filter(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.UPDATED_ON_GT: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        assert list(filterset.qs) == [self.future_record]

    def test_updated_on_lt_filter(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.CREATED_ON_LT: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        assert list(filterset.qs) == [self.past_record]

    def test_updated_on_gte_filter(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.UPDATED_ON_GTE: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        assert set(filterset.qs) == {self.present_record, self.future_record}

    def test_updated_on_lte_filter(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.UPDATED_ON_LTE: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        assert set(filterset.qs) == {self.past_record, self.present_record}

    def test_invalid_datetime_format(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.CREATED_ON: 'invalid-datetime'},
                                                   queryset=Criteria.objects.all())
        assert not filterset.is_valid()

    def test_combined_filters(self):
        filterset = PrivateUniqueResourceFilterSet({PrivateUniqueResourceFields.CREATED_ON_GTE: self.past.isoformat(),
                                                    PrivateUniqueResourceFields.CREATED_ON_LTE: self.now.isoformat(),
                                                    PrivateUniqueResourceFields.UPDATED_ON_GTE: self.past.isoformat(),
                                                    PrivateUniqueResourceFields.UPDATED_ON_LTE: self.now.isoformat()},
                                                   queryset=Criteria.objects.all())
        print('HOOOOOOOO')
        print(Criteria.objects.all())
        assert set(filterset.qs) == {self.past_record, self.present_record}
