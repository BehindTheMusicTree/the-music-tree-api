
from abc import abstractmethod
from typing import Dict, Optional

from django.core.exceptions import ImproperlyConfigured

"""
Rating Compatibility Table Across Different Audio Players

The following table shows how different audio players handle ratings across various audio formats.
Values represent the actual numbers written to files for each star rating (0-5 stars).

+-------+----------------+---------------+-----------------+---------------+--------------+-----------+
| Stars |  kid3/Lollypop |      WMP      |     MusicBee    |     Winamp    |    Traktor   |   iTunes  |
|       | mp3  wav  flac | mp3  wav flac | mp3  wav  flac  | mp3  wav flac | mp3 wav flac |Don't write|
|       |id3v2 riff vorb.|id3v2  ✗  vorb.|id3v2 id3v2 vorb.|id3v2  ✗  vorb.|id3v2 ✗  vorb.|rating tags|
+-------+----------------+---------------+-----------------+---------------+--------------+-----------+
| None  |  ✗    ✗    ✗   |  ✗         ✗  |  ✗    ✗    ✗    |  ✗        ✗   |  0        0  |           |
|  0    |                |               |  0    0    0    |               |              |           |
| 0.5   |                |               | 13   10   10    |               |              |           |
|  1    |  1    1    20  |  1         20 |  1   20   20    |  1        20  | 51        51 |           |
| 1.5   |                |               | 54   30   30    |               |              |           |
|  2    | 64    64   40  | 64         40 | 64   40   40    | 64        40  |102       102 |           |
| 2.5   |                |               |118   50   50    |               |              |           |
|  3    | 128   128  60  | 128        60 |128   60   60    | 128       60  |153       153 |           |
| 3.5   |                |               |186   70   70    |               |              |           |
|  4    | 196   196  80  | 196        80 |196   80   80    | 196       80  |204       204 |           |
| 4.5   |                |               |242   90   90    |               |              |           |
|  5    | 255   255  100 | 255       100 |255  100  100    | 255       100 |255       255 |           |
+-------+----------------+---------------+-----------------+---------------+--------------+-----------+

Legend:
✗ = No tag written
  = Rating value not supported
✓ = Can write ratings

Rating scale type:
- 255 star: Values 0-255 representing star ratings
- 100 prop: Values 0-100 representing proportional ratings
- 255 prop: Values 0-255 representing proportional ratings
"""

from ...utils.AppMetadataKey import AppMetadataKey
from ...utils.AudioFile import AudioFile
from ...utils.types import AppMetadataDict, AppMetadataValue, RawMetadataKey
from ..MetadataManager import MetadataManager
from ...utils.RatingProfile import RatingProfile


class RatingSupportingMetadataManager(MetadataManager):

    BASE_255_RATING_STAR_VALUES = [0, 13, 1, 54, 64, 118, 128, 186, 196, 242, 255]
    BASE_255_PROPORTIONAL_RATING_STAR_VALUES = [None, None, 51, None, 102, None, 153, None, 204, None, 255]
    BASE_100_RATING_STAR_VALUES = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    TRAKTOR_RATING_TAG_MAIL = 'traktor@native-instruments.de'

    normalized_rating_max_value: Optional[int]
    rating_profile: RatingProfile

    def __init__(self,
                 audio_file: AudioFile,
                 metadata_keys_direct_map: Dict[AppMetadataKey, Optional[RawMetadataKey]],
                 rating_profile: RatingProfile,
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

    def _get_undirectly_mapped_metadata_value(self, app_metadata_key: AppMetadataKey) -> Optional[AppMetadataValue]:
        if app_metadata_key == AppMetadataKey.RATING:
            return self._get_eventually_normalized_rating_from_file()
        else:
            return self._get_undirectly_mapped_metadata_value_other_than_rating(app_metadata_key)

    def _convert_normalized_rating_to_file_rating(self, normalized_rating: int, rating_profile: RatingProfile) -> int:
        if not self.normalized_rating_max_value:
            raise ImproperlyConfigured(
                "normalized_rating_max_value must be set to convert normalized rating to file rating.")

        star_rating_base_10 = (int)((normalized_rating * 10)/self.normalized_rating_max_value)
        if rating_profile == RatingProfile.BASE_255:
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
                        normalized_rating=normalized_rating, rating_profile=RatingProfile.BASE_100)
                    app_metadata_dict[AppMetadataKey.RATING] = file_rating
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid rating value: {value}. Expected a numeric value.")

        super().update_bulk(app_metadata_dict)
