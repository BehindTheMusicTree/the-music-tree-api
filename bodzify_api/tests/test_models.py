from django.test import TestCase
from django.contrib.auth.models import User

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.CriteriaType import CriteriaType

class CriteriaTestCase(TestCase):
    fixtures = ['initial_data']

    def createCriteria(self, name, type, allGenreCriteria, user):
        return Criteria.objects.create(
            name=name,
            type=type,
            parent=allGenreCriteria,
            user=user)

    def test_criterias(self):
        user = User.objects.get(username="admin")
        name = "Rap"
        type = CriteriaType.objects.get(pk=1)
        allGenreCriteria = Criteria.objects.get(type=type, parent=None, user=user)

        criteria = self.createCriteria(
            name=name, 
            type=type, 
            allGenreCriteria=allGenreCriteria, 
            user=user)
        self.assertTrue(isinstance(criteria, Criteria))
        self.assertIn(criteria.uuid + " " + criteria.name, str(criteria))