#!/usr/bin/env python

from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import status

from bodzify_api.model.Play import Play
from bodzify_api.serializer.play.output.detailed import Fields as GetFields
from bodzify_api.test.AppTestCase import AppTestCase


class PlayTestCase(AppTestCase):

    def _set_saved_play_attribute(self, response):
        uuid = response.json()[GetFields.UUID]
        self.saved_play = Play.objects.get(uuid=uuid)

    def post_play(self, data_dict):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.post(path=reverse('play-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_play_attribute(response)
        return response
