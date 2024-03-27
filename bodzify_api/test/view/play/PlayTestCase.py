#!/usr/bin/env python

import logging
from typing import Optional
from django.urls import get_resolver

from django.urls import reverse
from rest_framework import status

from bodzify_api import AudioMetadataManager
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.play.Play import Play
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.view.viewset.model.AppModelViewSet import PAGINATED_RESPONSE_FIELDS
from bodzify_api.serializer.track.input.schema.LibTrackExtractSerializer import FIELDS as LIB_TRACK_EXTRACT_FIELDS
from bodzify_api.serializer.track.input.schema.LibTrackPostSerializer import FIELDS as LIB_TRACK_POST_FIELDS
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import FIELDS as LIB_TRACK_GET_FIELDS
from bodzify_api.serializer.play.output.PlayDetailedSerializer import FIELDS as GET_FIELDS


logger = logging.getLogger('bodzify_api')


class PlayTestCase(ApiTestCase):

    def _set_saved_play_attribute(self, response):
        uuid = response.json()[GET_FIELDS.UUID]
        self.saved_play = Play.objects.get(uuid=uuid)

    def post_play(self, data_dict):
        response = self.api_client.post(path=reverse('play-list'),
                                        data=self._replace_none_values_by_empty_string(data_dict),
                                        format='json')
        if response.status_code == status.HTTP_201_CREATED:  # type: ignore
            self._set_saved_play_attribute(response)
        return response
