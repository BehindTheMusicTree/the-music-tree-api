#!/usr/bin/env python
from django.urls import reverse
from bodzify_api.test.view.ViewTestCase import ViewTestCase


class PlaylistViewTestCase(ViewTestCase):

    def get(self, playlistUuid):
        return self.apiClient.get(path=reverse('playlist-detail', kwargs={'pk': playlistUuid}))
