#!/usr/bin/env python

import logging
from typing import Optional
from urllib.parse import urlencode
from django.urls import get_resolver

from django.urls import reverse
from rest_framework import status

import bodzify_api.utils.audio_metadata as audio_metadata
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.playlist.children.SimplePlaylist import SimplePlaylist
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.test.AppTestCase import AppTestCase
from bodzify_api.view.viewset.model.AppModelViewSet import PAGINATED_RESPONSE_FIELDS
from bodzify_api.serializer.track.input.endpoint.extract import Fields as LIB_TRACK_EXTRACT_FIELDS
from bodzify_api.serializer.track.input.endpoint.post import Fields as LIB_TRACK_POST_FIELDS
from bodzify_api.serializer.track.output.detailed import Fields as LIB_TRACK_GET_FIELDS
from bodzify_api.serializer.playlist.children.simple.output.with_tracks \
    import Fields as SIMPLE_PLAYLIST_GET_FIELDS


class CriteriaTestCase(AppTestCase):
    saved_genre: Criteria

    def _set_saved_genre_attribute(self, response):
        uuid = response.json()[SIMPLE_PLAYLIST_GET_FIELDS.UUID]
        self.saved_genre = Criteria.objects.get(uuid=uuid)

    def retrieve_genre(self, uuid: str):
        response = self.api_client.get(path=reverse('genre-detail', kwargs={'pk': uuid}))
        if response.status_code == status.HTTP_200_OK:
            self._set_result(response=response)
        return response

    def get_genres(self):
        response = self.api_client.get(path=reverse('genre-list'))
        if response.status_code == status.HTTP_200_OK:
            self._set_results_attributes(response)
        return response

    def post_genre(self, data_dict):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.post(path=reverse('genre-list'),
                                        data=data_url_encoded,
                                        content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_201_CREATED:
            self._set_saved_genre_attribute(response)
        return response

    def put_genre(self, genre_uuid, data_dict):
        data_url_encoded = urlencode(self._replace_none_values_by_empty_string(data_dict), doseq=True)
        response = self.api_client.put(path=reverse('genre-detail', kwargs={'pk': genre_uuid}),
                                       data=data_url_encoded,
                                       content_type='application/x-www-form-urlencoded')
        if response.status_code == status.HTTP_200_OK:
            self._set_saved_genre_attribute(response)
        return response
