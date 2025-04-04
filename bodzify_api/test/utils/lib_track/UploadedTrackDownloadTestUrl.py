from enum import Enum


class UploadedTrackDownloadTestUrl(str, Enum):
    WAV = "http://www.canadianmusicartists.com/sample/fx02.wav"
    MP3 = "https://lasonotheque.org/UPLOAD/mp3/0001.mp3"
    LONG_MP3 = ("https://cs9-7v4.vkuseraudio.net/s/v1/acmp/i18p_zFWiH7jmzEvvkfhv21apWdJuIW5LJox"
                + "oSpJB9lqmTJK0HsSL7ZMerTX11oDXuFyCHXiqBZS5uKvikGDbs6Gcj1pinujYLx4JURjpPwxIIPE"
                + "_KN414JidBikY2vr290mJGqYNS544KrzQ1v-dqVY2hRtEfeoqwlRhgJQ3KpZMhmV2A.mp3")
    INVALID = "https://wrong-url_OIJOIEFHPOEIHFEPOFIHEOFIH.mp3"

    def __str__(self) -> str:
        return str(self.value)
