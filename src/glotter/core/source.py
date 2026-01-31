"""Source information"""

import os

from glotter.core.testinfo import TestInfo


class CoreSource:
    """Metadata about a source file

    :param name: filename including extension
    :param language: the language of the source
    :param path: path to the file excluding name
    :param test_info_string: a string in yaml format containing testinfo for a directory

    :ivar name: filename including extension
    :ivar path: path to the file excluding name
    :ivar language: the language of the source
    :ivar test_info: TestInfo object
    """

    def __init__(self, name, language, path, test_info_string):
        self._name = name
        self._language = language
        self._path = path

        self._test_info = TestInfo.from_string(test_info_string, self)

    @property
    def full_path(self) -> str:
        """Returns the full path to the source including filename and extension"""
        return os.path.join(self._path, self._name)

    @property
    def path(self):
        """Returns the path to the source excluding name"""
        return self._path

    @property
    def name(self) -> str:
        """Returns the name of the source excluding the extension"""
        return self._name.split(".")[0]

    @property
    def language(self) -> str:
        """Returns the language of the source"""
        return self._language

    @property
    def extension(self) -> str:
        """Returns the extension of the source"""
        return ".".join(["", *self._name.split(".")[1:]])

    @property
    def test_info(self) -> TestInfo:
        """Returns parsed TestInfo object"""
        return self._test_info

    def __repr__(self):
        return f"Source(name: {self.name}, path: {self.path})"


__all__ = ["CoreSource"]
