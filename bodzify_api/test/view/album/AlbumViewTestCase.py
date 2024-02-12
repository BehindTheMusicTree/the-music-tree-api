#!/usr/bin/env python
from django.urls import reverse
from bodzify_api.test.view.ViewTestCase import ViewTestCase


class AlbumViewTestCase(ViewTestCase):

    def delete(self, albumUuid: str):
        return self.api_client.delete(path=reverse('album-detail', kwargs={'pk': albumUuid}))
