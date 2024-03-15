#!/usr/bin/env python
from django.urls import reverse
from bodzify_api.test.AppTestCase import AppTestCase


class ArtistViewTestCase(AppTestCase):

    def _delete(self, artistUuid: str):
        return self.api_client.delete(path=reverse('artist-detail', kwargs={'pk': artistUuid}))
