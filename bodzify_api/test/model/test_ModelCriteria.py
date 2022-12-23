from django.test import TestCase
from django.contrib.auth.models import User

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaType, CriteriaTypesIds


USER_TEST_PK = 2

class CriteriaTestCase(TestCase):

    fixtures = ['initial_data', 'TestUserData']

    def createGenreCriteria(self, name, parent, user, type):
        return Criteria.objects.create(
            name=name,
            type=type,
            parent=parent,
            user=user)


    def test_criterias(self):
        userTest = User.objects.get(pk=USER_TEST_PK)
        name = "Rap"
        type = CriteriaType.objects.get(pk=CriteriaTypesIds.GENRE)
        allGenreCriteria = Criteria.objects.get(type=type, parent=None, user=userTest)
        criteria = self.createGenreCriteria(
            name=name,
            parent=allGenreCriteria,
            user=userTest,
            type=type)
        assert isinstance(criteria, Criteria) is True
        assert criteria.uuid + " " + criteria.name, str(criteria) is True