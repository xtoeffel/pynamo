"""Base classes for IO.
"""
from typing import Any


class FileTypeError(OSError):
    """Raised if a file extension or a file type is not supported."""

    @classmethod
    def by_path(cls, file_path: str, expected_extension: str):
        """Creates error by file path and expected file extension.

        :param file_path: file path of the file causing the file type error
        :type file_path: str

        :param expected_extension: expected file extension or type -- '.' will be prefixed if not present
        :type expected_extension: str
        """
        if not expected_extension[0] == ".":
            expected_extension = "." + expected_extension
        return FileTypeError(
            f'Invalid file type (extension) for "{file_path}", expected'
            f" {expected_extension}"
        )

    pass


class BaseReader:
    """Reader for models and other data."""

    # TODO: change return type to Dict[str, Any] or @dataclass that is more concrete?
    def read(self) -> Any:
        """Reads data from source and returns it."""
        raise NotImplementedError(f"{BaseReader.__class__.__name__}.read()")


class BaseWriter:
    """Writer for result files or any other data."""

    def write(self, **kwargs: Any) -> None:
        """Writes data to target."""
        raise NotImplementedError(f"{BaseWriter.__class__.__name__}.write()")
