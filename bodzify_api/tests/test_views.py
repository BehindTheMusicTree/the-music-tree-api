from django.urls import reverse
from django.test import TestCase
from django.test import Client


class ViewTestCase(TestCase):

    fixtures = ['initial_data', 'test_data']

    def test_view(self):
        client = Client()
        data = {
            "username": "user_test", 
            "password": "user_test"
        }
        response = client.post(
            reverse("token-obtain-pair"),
            data
        )
        assert response.status_code == 200
