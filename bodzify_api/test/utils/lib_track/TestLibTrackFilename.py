from enum import Enum


class TestLibTrackFilename(str, Enum):
    ALBUM_ARTISTS_MUSE_ID3V2_MP3 = "album artists=muse_id3v2.mp3"

    ALBUM_KOKO_ID3V2_MP3 = "album=koko_id3v2.mp3"
    ALBUM_KOKO_ID3V2_WAV = "album=koko_id3v2.wav"
    ALBUM_KOKO_VORBIS_FLAC = "album=koko_vorbis.flac"

    BITRATE_1411_FLAC = "bitrate=1411.flac"

    COPYRIGHT_DOMAINE_PUBLIC_RIFF_WAV = "copyright=domaine public_riff.wav"

    DEFAULT_MP3 = "default.mp3"

    DURATION_LESS_THAN_1_SEC_FLAC = "duration < 1 sec.flac"
    DURATION_LESS_THAN_1_SEC_MP3 = "duration < 1 sec.mp3"
    DURATION_LESS_THAN_1_SEC_WAV = "duration < 1 sec.wav"
    DURATION_1S_ISSUE_READING_FROM_MUTAGEN_AND_TYNITAG_WAV = "duration=1s issue reading from mutagen and tynitag.wav"
    DURATION_1S_MP3 = "duration=1s.wav"
    DURATION_277S_MP3 = "duration=277s.mp3"
    DURATION_335S_FLAC = "duration=335s.flac"
    DURATION_472S_WAV = "duration=472s.wav"

    FILENAME_DODIDO_MYFREEMP3_VIP_MP3 = "filename=dodido myfreemp3.vip .mp3"
    FILENAME_DOT_IN_FILENAME_MP3 = "filename=dot.in.filename.mp3"
    FILENAME_DOT_IN_FILENAME_WAV = "filename=with spaces  .mp3"
    FILENAME_DOT_NOT_IN_FILENAME_MP3 = "filename=dotnotinfilename.mp3"
    FILENAME_150_LONG_MP3 = \
        "kwPD6Zd3y5hQxbyFbNq895XZyFf7ycvJJ0Nf4vK5cFX5vt53fB8670j63Mx2ruMgVZ46B78iqu6vQpJ7hytZLbbv5Q1L6tiP6MfZAFRnidA8RrEKPnCxbNRUkQtdzBub7TW5zn0MuKqX5GzGd5.mp3"
    FILENAME_151_MP3 = \
        "kwPD6Zd3y5hQxbyFbNq895XZyFf7ycvJJ0Nf4vK5cFX5vt53fB8670j63Mx2ruMgVZ46B78iqu6vQpJ7hytZLbbv5Q1L6tiP6MfZAFRnidA8RrEKPnCxbNRUkQtdzBub7TW5zn0MuKqX5GzGd51.mp3"
    FILENAME_SPACES_TRAILING_MP3 = "filename= with spaces .mp3"

    FINGERPRINT_MP3 = "fingerprint.mp3"
    FINGERPRINT_WAV = "fingerprint.wav"

    FORMAT_BAD_EXTENSION_MP4 = "format=bad_extension.mp4"
    FORMAT_BAD_CONTENT_MP3 = "format=bad.mp3"
    FORMAT_IMAGE_JPEG = "format=image.jpeg"
    FORMAT_IN_MEMORY_FLAC = "format=in_memory.flac"
    FORMAT_MD5_NOT_VALID_AND_CORRUPTED_FLAC = "format=md5_not_valid_and_corrupted.flac"
    FORMAT_MD5_NOT_VALID_FLAC = "format=md5_not_valid.flac"

    GENRE_ABSTRACT_ID3V1_MP3 = "genre=abstract_id3v1.mp3"

    METADATA_MAX_A_ID3V2_FLAC = "metadata=max a_id3v2.flac"
    METADATA_MAX_A_ID3V2_WAV = "metadata=max a_id3v2.wav"
    METADATA_MAX_A_ID3v2_MP3 = "metadata=max a_id3v2.mp3"

    METADATA_NONE_FLAC = "metadata=none.flac"
    METADATA_NONE_MP3 = "metadata=none.mp3"
    METADATA_NONE_WAV = "metadata=none.wav"

    METADATA_WITH_ID3V2_WAV = "metadata=with_id3v2.wav"

    RATING_ID3V2_KID3_1_STAR_WAV = "rating_id3v2_kid3=1 star.wav"
    RATING_ID3V2_KID3_2_STAR_WAV = "rating_id3v2_kid3=2 star.wav"
    RATING_ID3V2_KID3_3_STAR_WAV = "rating_id3v2_kid3=3 star.wav"
    RATING_ID3V2_KID3_4_STAR_WAV = "rating_id3v2_kid3=4 star.wav"
    RATING_ID3V2_KID3_5_STAR_WAV = "rating_id3v2_kid3=5 star.wav"

    RATING_ID3V2_MUSICBEE_0_STAR_WAV = "rating_id3v2_musicbee=0 star.wav"
    RATING_ID3V2_MUSICBEE_0_5_STAR_WAV = "rating_id3v2_musicbee=0.5 star.wav"
    RATING_ID3V2_MUSICBEE_1_STAR_WAV = "rating_id3v2_musicbee=1 star.wav"
    RATING_ID3V2_MUSICBEE_1_5_STAR_WAV = "rating_id3v2_musicbee=1.5 star.wav"
    RATING_ID3V2_MUSICBEE_2_STAR_WAV = "rating_id3v2_musicbee=2 star.wav"
    RATING_ID3V2_MUSICBEE_2_5_STAR_WAV = "rating_id3v2_musicbee=2.5 star.wav"
    RATING_ID3V2_MUSICBEE_3_STAR_WAV = "rating_id3v2_musicbee=3 star.wav"
    RATING_ID3V2_MUSICBEE_3_5_STAR_WAV = "rating_id3v2_musicbee=3.5 star.wav"
    RATING_ID3V2_MUSICBEE_4_STAR_WAV = "rating_id3v2_musicbee=4 star.wav"
    RATING_ID3V2_MUSICBEE_4_5_STAR_WAV = "rating_id3v2_musicbee=4.5 star.wav"
    RATING_ID3V2_MUSICBEE_5_STAR_WAV = "rating_id3v2_musicbee=5 star.wav"

    RATING_ID3V2_0_STAR_FLAC = "rating_id3v2=0 star.flac"
    RATING_ID3V2_0_STAR_MP3 = "rating_id3v2=0 star.mp3"

    RATING_ID3V2_0_5_STAR_FLAC = "rating_id3v2=0.5 star.flac"
    RATING_ID3V2_0_5_STAR_MP3 = "rating_id3v2=0.5 star.mp3"

    RATING_ID3V2_1_STAR_FLAC = "rating_id3v2=1 star.flac"
    RATING_ID3V2_1_STAR_MP3 = "rating_id3v2=1 star.mp3"

    RATING_ID3V2_1_5_STAR_FLAC = "rating_id3v2=1.5 star.flac"
    RATING_ID3V2_1_5_STAR_MP3 = "rating_id3v2=1.5 star.mp3"
    RATING_ID3V2_1_5_STAR_WAV = "rating_id3v2=1.5 star.wav"

    RATING_ID3V2_2_STAR_FLAC = "rating_id3v2=2 star.flac"
    RATING_ID3V2_2_STAR_MP3 = "rating_id3v2=2 star.mp3"

    RATING_ID3V2_2_5_STAR_FLAC = "rating_id3v2=2.5 star.flac"
    RATING_ID3V2_2_5_STAR_MP3 = "rating_id3v2=2.5 star.mp3"
    RATING_ID3V2_2_5_STAR_WAV = "rating_id3v2=2.5 star.wav"

    RATING_ID3V2_3_STAR_FLAC = "rating_id3v2=3 star.flac"
    RATING_ID3V2_3_STAR_MP3 = "rating_id3v2=3 star.mp3"

    RATING_ID3V2_3_5_STAR_FLAC = "rating_id3v2=3_5 star.flac"
    RATING_ID3V2_3_5_STAR_MP3 = "rating_id3v2=3_5 star.mp3"
    RATING_ID3V2_3_5_STAR_WAV = "rating_id3v2=3_5 star.wav"

    RATING_ID3V2_4_STAR_FLAC = "rating_id3v2=4 star.flac"
    RATING_ID3V2_4_STAR_MP3 = "rating_id3v2=4 star.mp3"

    RATING_ID3V2_5_STAR_FLAC = "rating_id3v2=5 star.flac"
    RATING_ID3V2_5_STAR_MP3 = "rating_id3v2=5 star.mp3"

    RATING_ID3V2_TRACKTOR_1_STAR_MP3 = "rating_id3v2_tracktor=1 star.mp3"
    RATING_ID3V2_TRACKTOR_2_STAR_MP3 = "rating_id3v2_tracktor=2 star.mp3"
    RATING_ID3V2_TRACKTOR_3_STAR_MP3 = "rating_id3v2_tracktor=3 star.mp3"
    RATING_ID3V2_TRACKTOR_4_STAR_MP3 = "rating_id3v2_tracktor=4 star.mp3"
    RATING_ID3V2_TRACKTOR_5_STAR_MP3 = "rating_id3v2_tracktor=5 star.mp3"
    RATING_ID3V2_TRACKTOR_NONE_MP3 = "rating_id3v2_tracktor=none.mp3"

    RATING_ID3V2_NONE_WAV = "rating_id3v2=none.wav"

    RATING_VORBIS_0_5_STAR_FLAC = "rating_vorbis=0.5 star.flac"
    RATING_VORBIS_0_STAR_FLAC = "rating_vorbis=0 star.flac"
    RATING_VORBIS_1_5_STAR_FLAC = "rating_vorbis=1.5 star.flac"
    RATING_VORBIS_1_STAR_FLAC = "rating_vorbis=1 star.flac"
    RATING_VORBIS_2_5_STAR_FLAC = "rating_vorbis=2.5 star.flac"
    RATING_VORBIS_2_STAR_FLAC = "rating_vorbis=2 star.flac"
    RATING_VORBIS_3_5_STAR_FLAC = "rating_vorbis=3.5 star.flac"
    RATING_VORBIS_3_STAR_FLAC = "rating_vorbis=3 star.flac"
    RATING_VORBIS_4_5_STAR_FLAC = "rating_vorbis=4.5 star.flac"
    RATING_VORBIS_4_STAR_FLAC = "rating_vorbis=4 star.flac"
    RATING_VORBIS_5_STAR_FLAC = "rating_vorbis=5 star.flac"

    RATING_VORBIS_TRAKTOR_1_STAR_FLAC = "rating_vorbis_traktor=1 star.flac"
    RATING_VORBIS_TRAKTOR_2_STAR_FLAC = "rating_vorbis_traktor=2 star.flac"
    RATING_VORBIS_TRAKTOR_3_STAR_FLAC = "rating_vorbis_traktor=3 star.flac"
    RATING_VORBIS_TRAKTOR_4_STAR_FLAC = "rating_vorbis_traktor=4 star.flac"
    RATING_VORBIS_TRAKTOR_5_STAR_FLAC = "rating_vorbis_traktor=5 star.flac"
    RATING_VORBIS_TRAKTOR_NONE_FLAC = "rating_vorbis_traktor=none.flac"

    RECORDING_ALLUMERLEFEU_2_MATCHES_ONE_WITH_MORE_RELEASE_GROUPS_MP3 = \
        "recording=Allumerlefeu_2 matches one with more release groups.mp3"
    RECORDING_CELINEKIN_PARK_NO_MUSICBRAINZ_RECORDING_DURATION_MP3 = \
        "recording=Celinekin Park - no musicbrainz recording duration.mp3"
    RECORDING_DANS_LA_LEGENDE_FLAC = "recording=Dans la legende.flac"

    RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M20_FLAC = \
        "recording=juan hansen oostil - drown (massano remix) - 7m20.flac"
    RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3 = \
        "recording=juan hansen oostil - drown (massano remix) - 7m21.mp3"

    RECORDING_KEMAR_FRANCE_MP3 = "recording=Kemar - France.mp3"
    RECORDING_LORIE_2_MATCHES_BUT_ONE_WITH_CLOSEST_DURATION_MP3 = \
        "recording=lorie_2_matches_but_one_with_closest_duration.mp3"
    RECORDING_QUEEN_25_MATCHES_BUT_ONE_WITH_BEST_DURATION_AND_MOST_FIELDS_AND_MOST_RELEASE_GROUPS_MP3 = \
        "recording=queen_25_matches_but_one_with_best_duration_and_most_fields_and_most_release_groups.mp3"
    RECORDING_QUEEN_DURATION_181_MP3 = "recording=queen_duration_181.mp3"
    RECORDING_QUEEN_MULTIPLE_RELEASE_DATES_MP3 = "recording=queen_multiple_release_dates.mp3"
    RECORDING_QUEEN_WEARETHECHAMPIONS_MP3 = "recording=queen_wearethechampions.mp3"
    RECORDING_SHOWMUSTGOON_MP3 = "recording=showmustgoon.mp3"
    RECORDING_CALIFORNIA_GURLS_ID3V2_TAGS_FLAC = "recording=california gurls_id3v2 tags.flac"
    RECORDING_TOKYO_DRIFT_NO_MUSICBRAINZ_RECORDING_MP3 = "recording=Tokyo Drift_no mb recording.mp3"

    RECORDING_TOTAL_ECLIPSE_5M35_FLAC = "recording=total eclipse_5m35.flac"
    RECORDING_TOTAL_ECLIPSE_3_SCORES_FLAC = "recording=total eclipse_3 scores.flac"
    RECORDING_TOTAL_ECLIPSE_9_MATCHES_BUT_ONE_WITH_DURATION_FLAC = \
        "recording=total eclipse_9 matches one with duration.flac"

    RECORDING_CARMINA_BURANA_REMIX_7M52_MP3 = "recording=Y do i - Carmina Burana Remix - 7m52.mp3"
    RECORDING_CARMINA_BURANA_REMIX_7M52_WAV = "recording=Y do i - Carmina Burana Remix - 7m52.wav"

    def __str__(self) -> str:
        return str(self.value)
