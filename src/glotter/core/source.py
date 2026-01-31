"""Source information"""

import os
from dataclasses import dataclass, field

from glotter.core.testinfo import TestInfo


@dataclass(frozen=True)
class CoreSource:
    """Metadata about a source file

    :ivar fullname: filename including extension
    :ivar language: the language of the source
    :ivar path: path to the file excluding name
    :ivar test_info: TestInfo object
    """

    filename: str
    language: str
    path: str
    test_info: TestInfo = field(repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "test_info", TestInfo.from_string(self.test_info, self))

    @property
    def full_path(self) -> str:
        """Returns the full path to the source including filename and extension"""
        return os.path.join(self.path, self.filename)

    @property
    def name(self) -> str:
        """Returns the name of the source excluding the extension"""
        return self.filename.split(".")[0]

    @property
    def extension(self) -> str:
        """Returns the extension of the source"""
        return ".".join(["", *self.filename.split(".")[1:]])


__all__ = ["CoreSource"]
