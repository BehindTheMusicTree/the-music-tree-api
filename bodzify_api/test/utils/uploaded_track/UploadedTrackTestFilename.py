from enum import Enum


class UploadedTrackTestFilename(str, Enum):
    RATING_ID3V2_5_STAR_MP3 = "rating_id3v2_5_star.mp3"
    RATING_ID3V2_0_STAR_MP3 = "rating_id3v2_0_star.mp3"
    RATING_VORBIS_5_STAR_FLAC = "rating_vorbis_5_star.flac"
    RATING_VORBIS_0_STAR_FLAC = "rating_vorbis_0_star.flac"
    RATING_RIFF_BASE_100_KID3_5_STAR_WAV = "rating_riff_base_100_kid3_5_star.wav"
    RATING_ID3V2_TRACKTOR_5_STAR_MP3 = "rating_id3v2_traktor_5_star.mp3"
    RATING_VORBIS_TRAKTOR_5_STAR_FLAC = "rating_vorbis_traktor_5_star.flac"
