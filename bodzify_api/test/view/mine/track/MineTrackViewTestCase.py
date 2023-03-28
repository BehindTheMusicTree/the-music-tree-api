#!/usr/bin/env python
from django.urls import reverse
from rest_framework import status
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.view.ViewTestCase import ViewTestCase


class MineTrackExtractViewTestCase(ViewTestCase):

    def _loginAndExtract(self, data):
        self._login(self.testUser)
        response = self.apiClient.post(path=reverse('mine-track-extract'), data=data)
        if response.status_code == status.HTTP_201_CREATED:
            trackUuid = response.json()[LibraryTrack.ATTRIBUTE_UUID_LABEL]
            self.savedTrack = LibraryTrack.objects.get(uuid=trackUuid)
        return response
