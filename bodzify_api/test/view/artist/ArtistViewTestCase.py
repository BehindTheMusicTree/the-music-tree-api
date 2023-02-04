#!/usr/bin/env python

from django.urls import reverse

from bodzify_api.test.view.ViewTestCase import ViewTestCase


class ArtistViewTestCase(ViewTestCase):

    def delete(self, artistUuid):
        return self.apiClient.delete(path=reverse('artist-detail', kwargs={'pk': artistUuid}))
