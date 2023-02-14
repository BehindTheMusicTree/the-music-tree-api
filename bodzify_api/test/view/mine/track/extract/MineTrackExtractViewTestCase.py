#!/usr/bin/env python
from django.urls import reverse
from bodzify_api.test.view.ViewTestCase import ViewTestCase


class MineTrackExtractViewTestCase(ViewTestCase):

    def extract(self, data):
        return self.apiClient.post(
            path=reverse('mine-track-extract'), data=data)
