from api import settings
from api.serializer.model.track.input.Fields import Fields
from api.serializer.model.track.input.input import TrackInputSerializer
from api.utils import data_transformer, utils


class TrackPostSerializer(TrackInputSerializer):
    def _get_generated_title_from_data(self, data: dict):
        title = settings.TRACK_GENERATED_TITLE_PREFIXE + \
            utils.generate_short_uu(
                settings.TRACK_GENERATED_TITLE_LENGTH - len(settings.TRACK_GENERATED_TITLE_PREFIXE))
        return title

    def validate(self, data: dict):
        self._validate_album_fields_from_data(data)

        user = self.context['request'].user

        keys = [Fields.TITLE,
                Fields.ARTISTS_NAMES,
                Fields.ALBUM_NAME,
                Fields.ALBUM_ARTISTS_NAMES,
                Fields.TRACK_NUMBER,
                Fields.GENRE,
                Fields.RATING,
                Fields.LANGUAGE]

        input_data = data.copy()

        if input_data.get(Fields.TITLE) in [None, '']:
            input_data[Fields.TITLE] = self._get_generated_title_from_data(input_data)

        return super().validate(input_data)
