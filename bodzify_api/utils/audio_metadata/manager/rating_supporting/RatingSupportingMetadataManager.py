from abc import abstractmethod
from ..MetadataManager import MetadataManager
from ...utils.rating_profiles import RatingWritingProfile
from ...utils.types import AppMetadataDict, AppMetadataValue, RawMetadataKey
from ...utils.AudioFile import AudioFile
from ...utils.AppMetadataKey import AppMetadataKey
from django.core.exceptions import ImproperlyConfigured
from typing import Dict, Optional


class RatingSupportingMetadataManager(MetadataManager):

    TRAKTOR_RATING_TAG_MAIL = 'traktor@native-instruments.de'

    normalized_rating_max_value: Optional[int]
    rating_profile: RatingWritingProfile

    def __init__(self,
                 audio_file: AudioFile,
                 metadata_keys_direct_map: Dict[AppMetadataKey, Optional[RawMetadataKey]],
                 rating_profile: RatingWritingProfile,
                 normalized_rating_max_value: Optional[int]):
        self.rating_profile = rating_profile
        self.normalized_rating_max_value = normalized_rating_max_value
        super().__init__(audio_file, metadata_keys_direct_map)

    @abstractmethod
    def _extract_file_rating(self) -> Optional[int]:
        raise NotImplementedError()

    @abstractmethod
    def _extract_file_traktor_rating(self) -> Optional[int]:
        raise NotImplementedError()

    @abstractmethod
    def _get_undirectly_mapped_metadata_value_other_than_rating(
            self, key: AppMetadataKey) -> Optional[AppMetadataValue]:
        raise NotImplementedError()

    def _get_undirectly_mapped_metadata_value(self, app_metadata_key: AppMetadataKey) -> None | AppMetadataValue:
        if app_metadata_key == AppMetadataKey.RATING:
            return self._get_eventually_normalized_rating_from_file()
        else:
            return self._get_undirectly_mapped_metadata_value_other_than_rating(app_metadata_key)

    def _convert_normalized_rating_to_file_rating(
            self, normalized_rating: int, rating_writing_profile: RatingWritingProfile) -> int:
        if not self.normalized_rating_max_value:
            raise ImproperlyConfigured(
                "normalized_rating_max_value must be set to convert normalized rating to file rating.")

        star_rating_base_10 = (int)((normalized_rating * 10)/self.normalized_rating_max_value)
        if rating_writing_profile == RatingWritingProfile.BASE_255:
            return self.BASE_255_RATING_STAR_VALUES[star_rating_base_10]
        else:
            return self.BASE_100_RATING_STAR_VALUES[star_rating_base_10]

    def _get_eventually_normalized_rating_from_file(self) -> Optional[int]:
        file_rating = self._extract_file_rating()
        is_rating_from_traktor = False
        if file_rating is None:
            file_rating = self._extract_file_traktor_rating()
            if file_rating:
                is_rating_from_traktor = True

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
                if file_rating in [self.BASE_255_RATING_STAR_VALUES[star_rating_base_10],
                                   self.BASE_255_PROPORTIONAL_RATING_STAR_VALUES[star_rating_base_10],
                                   self.BASE_100_RATING_STAR_VALUES[star_rating_base_10]]:
                    return int(star_rating_base_10 * self.normalized_rating_max_value / 10)
            raise ValueError("Rating value not handled: " + str(file_rating))
        else:
            return file_rating

    def update_bulk(self, app_metadata_dict: AppMetadataDict):
        if AppMetadataKey.RATING in list(app_metadata_dict.keys()):
            value = app_metadata_dict[AppMetadataKey.RATING]
            if value is None:
                del app_metadata_dict[AppMetadataKey.RATING]
            else:
                if self.normalized_rating_max_value is None:
                    raise ImproperlyConfigured(
                        "If updating the rating, the max value of the normalized rating must be set.")

                try:
                    normalized_rating = int(float(value))
                    file_rating = self._convert_normalized_rating_to_file_rating(
                        normalized_rating=normalized_rating, rating_writing_profile=RatingWritingProfile.BASE_100)
                    app_metadata_dict[AppMetadataKey.RATING] = file_rating
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid rating value: {value}. Expected a numeric value.")

        super().update_bulk(app_metadata_dict)
