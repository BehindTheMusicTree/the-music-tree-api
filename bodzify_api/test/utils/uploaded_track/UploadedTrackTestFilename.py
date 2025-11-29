from enum import Enum


class UploadedTrackTestFilename(str, Enum):
    DEFAULT_MP3 = "rating_id3v2=5 star.mp3"
    RATING_ID3V2_5_STAR_MP3 = "rating_id3v2=5 star.mp3"
    RATING_ID3V2_0_STAR_MP3 = "rating_id3v2_0_star.mp3"
    RATING_VORBIS_5_STAR_FLAC = "rating_vorbis_5_star.flac"
    RATING_VORBIS_0_STAR_FLAC = "rating_vorbis_0_star.flac"
    RATING_RIFF_BASE_100_KID3_5_STAR_WAV = "rating_riff_base_100_kid3_5_star.wav"
    RATING_ID3V2_TRACKTOR_5_STAR_MP3 = "rating_id3v2_traktor_5_star.mp3"
    RATING_VORBIS_TRAKTOR_5_STAR_FLAC = "rating_vorbis_traktor_5_star.flac"
    METADATA_NONE_MP3 = "metadata=none.mp3"
    METADATA_NONE_WAV = "metadata=none.wav"
    METADATA_NONE_FLAC = "metadata=none.flac"
    METADATA_LONG_A_ID3V1_SMALL_MP3 = "metadata=long a_id3v1_small.mp3"
    METADATA_LONG_A_ID3V2_SMALL_MP3 = "metadata=long a_id3v2_small.mp3"
    METADATA_LONG_A_VORBIS_SMALL_FLAC = "metadata=long a_vorbis_small.flac"
    METADATA_LONG_A_RIFF_SMALL_WAV = "metadata=long a_riff_small.wav"
    RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3 = "recording=juan hansen oostil - drown (massano remix) - 7m21.mp3"
    RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M20_FLAC = "recording=juan hansen oostil - drown (massano remix) - 7m20.flac"
    RECORDING_ALLUMERLEFEU_2_MATCHES_ONE_WITH_MORE_RELEASE_GROUPS_MP3 = "recording=Allumerlefeu_2 matches one with more release groups.mp3"
    RECORDING_KEMAR_FRANCE_MP3 = "recording=Kemar - France.mp3"
