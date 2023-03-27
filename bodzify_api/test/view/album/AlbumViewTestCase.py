#!/usr/bin/env python
from django.urls import reverse
from bodzify_api.test.view.ViewTestCase import ViewTestCase


class AlbumViewTestCase(ViewTestCase):

    def _loginAndDelete(self, albumUuid: str):
        self._login(self.testUser)
        return self.apiClient.delete(path=reverse('album-detail', kwargs={'pk': albumUuid}))
