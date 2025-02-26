from abc import abstractmethod

from django.core.exceptions import ImproperlyConfigured

from ....AudioFile import AudioFile
from ...utils.AppMetadataKey import AppMetadataKey
from ...utils.rating_profiles import RatingReadProfile, RatingWriteProfile
from ...utils.types import AppMetadataDict, MetadataValue, RawMetadataKey
from ..MetadataManager import MetadataManager


class RatingSupportingMetadataManager(MetadataManager):

    TRAKTOR_RATING_TAG_MAIL = 'traktor@native-instruments.de'

    normalized_rating_max_value: int | None
    rating_write_profile: RatingWriteProfile

    def __init__(self, audio_file: AudioFile,
                 metadata_keys_direct_map_read: dict[AppMetadataKey, RawMetadataKey | None],
                 metadata_keys_direct_map_write: dict[AppMetadataKey, RawMetadataKey | None],
                 rating_write_profile: RatingWriteProfile,
                 normalized_rating_max_value: int | None):

        self.rating_write_profile = rating_write_profile
        self.normalized_rating_max_value = normalized_rating_max_value
        super().__init__(audio_file=audio_file,
                         metadata_keys_direct_map_read=metadata_keys_direct_map_read,
                         metadata_keys_direct_map_write=metadata_keys_direct_map_write)

    @abstractmethod
    def _extract_file_rating_by_traktor_or_not(self) -> tuple[int | None, bool]:
        """
        Returns True if the rating is from Traktor, False otherwise.
        """
        raise NotImplementedError()

    @abstractmethod
    def _get_undirectly_mapped_metadata_value_other_than_rating(
            self, key: AppMetadataKey) -> MetadataValue:
        raise NotImplementedError()

    def _get_undirectly_mapped_metadata_value(self, app_metadata_key: AppMetadataKey) -> MetadataValue | None:
        if app_metadata_key == AppMetadataKey.RATING:
            return self._get_eventually_normalized_rating_from_file()
        else:
            return self._get_undirectly_mapped_metadata_value_other_than_rating(app_metadata_key)

    def _convert_normalized_rating_to_file_rating(self, normalized_rating: int) -> int | None:
        if not self.normalized_rating_max_value:
            raise ImproperlyConfigured("normalized_rating_max_value must be set.")

        star_rating_base_10 = (int)((normalized_rating * 10)/self.normalized_rating_max_value)
        self.rating_write_profile[star_rating_base_10]

    def _get_eventually_normalized_rating_from_file(self) -> int | None:
        file_rating, is_rating_from_traktor = self._extract_file_rating_by_traktor_or_not()
        if file_rating is None or file_rating == "":
            return None
        else:
            return self._convert_file_rating_to_eventually_normalized_rating(
                file_rating=file_rating, is_rating_from_traktor=is_rating_from_traktor)

    def _convert_file_rating_to_eventually_normalized_rating(self,
                                                             file_rating: int,
                                                             is_rating_from_traktor: bool = False):
        if self.normalized_rating_max_value:
            if file_rating == 0 and is_rating_from_traktor:
                return None
            for star_rating_base_10 in range(11):
                if file_rating in [RatingReadProfile.BASE_255_PROPORTIONAL[star_rating_base_10],
                                   RatingReadProfile.BASE_255_NON_PROPORTIONAL[star_rating_base_10],
                                   RatingReadProfile.BASE_100_PROPORTIONAL[star_rating_base_10]]:
                    return int(star_rating_base_10 * self.normalized_rating_max_value / 10)
            return None
        else:
            return file_rating

    def update_bulk(self, app_metadata_dict: AppMetadataDict):
        if AppMetadataKey.RATING in list(app_metadata_dict.keys()):
            value: int | None = app_metadata_dict[AppMetadataKey.RATING]  # type: ignore
            if value is None:
                del app_metadata_dict[AppMetadataKey.RATING]
            else:
                if self.normalized_rating_max_value is None:
                    raise ImproperlyConfigured(
                        "If updating the rating, the max value of the normalized rating must be set.")

                try:
                    normalized_rating = int(float(value))
                    file_rating = self._convert_normalized_rating_to_file_rating(normalized_rating=normalized_rating)
                    app_metadata_dict[AppMetadataKey.RATING] = file_rating
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid rating value: {value}. Expected a numeric value.")

        super().update_bulk(app_metadata_dict)
