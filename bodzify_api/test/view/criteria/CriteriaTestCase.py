#!/usr/bin/env python

import logging
from typing import Optional
from urllib.parse import urlencode
from django.urls import get_resolver

from django.urls import reverse
from rest_framework import status

from bodzify_api import AudioMetadataManager
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.ApiTestCase import ApiTestCase
from bodzify_api.view.viewset.model.AppModelViewSet import PAGINATED_RESPONSE_FIELDS
from bodzify_api.serializer.track.input.endpoint.LibTrackExtractSerializer import FIELDS as LIB_TRACK_EXTRACT_FIELDS
from bodzify_api.serializer.track.input.endpoint.LibTrackPostSerializer import FIELDS as LIB_TRACK_POST_FIELDS
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import FIELDS as LIB_TRACK_GET_FIELDS
from bodzify_api.serializer.playlist.children.simple.output.SimplePlaylistWithTracksSerializer \
    import FIELDS as SIMPLE_PLAYLIST_GET_FIELDS


logger = logging.getLogger('bodzify_api')


class CriteriaTestCase(ApiTestCase):
    saved_genre: Criteria

    def _set_saved_genre_attribute(self, response):
        uuid = response.json()[SIMPLE_PLAYLIST_GET_FIELDS.UUID]
        self.saved_genre = Criteria.objects.get(uuid=uuid)

    def retrieve_genre(self, uuid: str):
        response = self.api_client.get(path=reverse('genre-detail', kwargs={'pk': uuid}))
        if response.status_code == status.HTTP_200_OK:  # type: ignore
            self._set_result(response=response)
        return response

    def get_genres(self):
        response = self.api_client.get(path=reverse('genre-list'))
        if response.status_code == status.HTTP_200_OK:  # type: ignore
            self._set_results_attributes(response)
        return response

    def post_genre(self, data_dict):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.post(path=reverse('genre-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:  # type: ignore
            self._set_saved_genre_attribute(response)
        return response

    def put_genre(self, genre_uuid, data_dict):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.put(path=reverse('genre-detail', kwargs={'pk': genre_uuid}),
                                       data=data_url_encoded,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:  # type: ignore
            self._set_saved_genre_attribute(response)
        return response
