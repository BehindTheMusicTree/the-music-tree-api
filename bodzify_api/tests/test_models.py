import pytest

from django.test import TestCase
from django.contrib.auth.models import User

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaType, CriteriaTypesIds

USER_TEST_PK = 2

@pytest.mark.django_db(transaction=True)
class CriteriaTestCase(TestCase):

    fixtures = ['initial_data', 'test_data']
    
    def createTestUser(self):
        User.objects.create_user(
            pk=USER_TEST_PK, 
            username="test", 
            password="test", 
            email="test@test.com"
        )

    def createGenreCriteria(self, name, user):
        type = CriteriaType.objects.get(pk=CriteriaTypesIds.GENRE)
        allGenreCriteria = Criteria.objects.get(type=type, parent=None, user=user)
        return Criteria.objects.create(
            name=name,
            type=type,
            parent=allGenreCriteria,
            user=user)

    def test_criterias(self):
        userTest = User.objects.get(pk=USER_TEST_PK)
        name = "Rap"
        criteria = self.createGenreCriteria(name=name, user=userTest)
        assert isinstance(criteria, Criteria) is True
        assert criteria.uuid + " " + criteria.name, str(criteria) is True