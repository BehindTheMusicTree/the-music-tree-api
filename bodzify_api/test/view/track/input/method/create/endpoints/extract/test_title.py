from rest_framework import status

from bodzify_api import settings
from bodzify_api.serializer.schema.model.lib_track.input.extract.Fields import Fields as ExtractFields
from bodzify_api.test.view.track.LibTrackTestCase import LibTrackTestCase


class TestCase(LibTrackTestCase):

    def test_not_providing_title_nor_artist_and_original_filename_too_long_then_generate_with_app_prefixe(self):
        track_url = (
            "https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
            + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE"
            + "_KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
        response = self._extract(**{ExtractFields.URL: track_url})

        assert response.status_code == status.HTTP_201_CREATED
        assert self.saved_object.title.startswith(settings.LIB_TRACK_GENERATED_TITLE_PREFIXE)
