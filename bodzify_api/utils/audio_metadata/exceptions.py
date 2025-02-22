class FileCorruptedError(Exception):
    pass


class FlacMd5CheckFailedError (FileCorruptedError):
    pass


class FileByteMismatchError(FileCorruptedError):
    pass


class InvalidChunkDecodeError(FileCorruptedError):
    pass


class FileTypeNotSupportedError(Exception):
    pass
