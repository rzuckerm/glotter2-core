"""Container, folder, and test information"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import yaml
from jinja2 import BaseLoader, Environment

from .project import CoreProjectMixin, NamingScheme


@dataclass(frozen=True)
class ContainerInfo:
    """Configuration for a container to run for a directory

    :ivar image: the image to run
    :ivar tag: the tag of the image to run
    :ivar cmd: the command to run the source inside the container
    :ivar build: an optional command to run to build the source before running the command
    """

    image: str = ""
    tag: str = ""
    cmd: str = ""
    build: Optional[str] = None

    @classmethod
    def from_dict(cls, dictionary: dict[str, Optional[str]]) -> ContainerInfo:
        """
        Create a ContainerInfo object from a dictionary

        :param dictionary: the dictionary representing ContainerInfo
        :return: a new ContainerInfo object
        """
        image = dictionary.get("image", "")
        tag = dictionary.get("tag", "")
        cmd = dictionary.get("cmd", "")
        build = dictionary.get("build")
        return ContainerInfo(image=image, tag=tag, cmd=cmd, build=build)

    def __bool__(self) -> bool:
        return bool(self.image and self.tag and self.cmd)


@dataclass(frozen=True)
class FolderInfo:
    """Metadata about sources in a directory

    :param extension: the file extension that is considered as source
    :param str naming: string containing the naming scheme for files in the directory
    :raises: :exc:`ValueError` if invalid naming scheme

    :ivar extension: the file extension that is considered as source
    :ivar NamingScheme naming: the naming scheme for files in the directory
    """

    extension: str
    naming: str

    def __post_init__(self) -> None:
        try:
            object.__setattr__(self, "naming", NamingScheme[self.naming])
        except KeyError as e:
            raise ValueError(f'Unknown naming scheme: "{self.naming}"') from e

    def get_project_mappings(
        self, projects: dict[str, CoreProjectMixin], include_extension: bool = False
    ) -> dict[str, str]:
        """
        Uses the naming scheme to generate the expected source names in the directory
        and create a mapping from project type to source name

        :param project: dictionary whose key is a project type and whose value is
            information about the project
        :param include_extension: whether to include the extension in the source name
        :return: a dict where the key is a ] and the value is the source name
        """
        extension = self.extension if include_extension else ""
        return {
            project_type: f"{project.get_project_name_by_scheme(self.naming)}{extension}"
            for project_type, project in projects.items()
        }

    @classmethod
    def from_dict(cls, dictionary: dict[str, str]) -> FolderInfo:
        """
        Create a FileInfo from a dictionary

        :param dictionary: the dictionary representing FileInfo
        :return: a new FileInfo
        """
        return FolderInfo(dictionary["extension"], dictionary["naming"])


@dataclass(frozen=True)
class TestInfo:
    """An object representation of a testinfo file

    :param container_info: ContainerInfo object
    :param file_info: FolderInfo object
    :param language_display_name: string indicating the display name of the
        language
    :param notes: a list of notes about the language

    :ivar container_info: ContainerInfo object
    :ivar file_info: FolderInfo object
    :ivar language_display_name: string indicating the display name of the
        language
    :ivar notes: a list of notes about the language
    """

    container_info: ContainerInfo
    file_info: FolderInfo
    language_display_name: str
    notes: list[str] = field(default_factory=list)

    __test__ = False  # Indicate this is not a test

    @classmethod
    def from_dict(cls, dictionary: dict[str, Any], language: str) -> TestInfo:
        """
        Create a TestInfo object from a dictionary

        :param dictionary: the dictionary representing a TestInfo object
        :param language: language of source object
        :return: a new TestInfo object
        """
        language_display_name = dictionary.get(
            "language_display_name", _get_language_display_name(language)
        )
        return TestInfo(
            container_info=ContainerInfo.from_dict(dictionary.get("container", {})),
            file_info=FolderInfo.from_dict(dictionary["folder"]),
            language_display_name=language_display_name,
            notes=dictionary.get("notes", []),
        )

    @classmethod
    def from_string(cls, string: str, source) -> TestInfo:
        """
        Create a TestInfo from a string. Modify the string using Jinja2 templating.
        Then parse it as yaml

        :param string: contents of a testinfo file
        :param source: a source object to use for jinja2 template parsing
        :param language: language of source
        :return: a new TestInfo
        """
        template = Environment(loader=BaseLoader).from_string(string)
        template_string = template.render(source=source)
        info_yaml = yaml.safe_load(template_string)
        return cls.from_dict(info_yaml, source.language)

    @property
    def is_testable(self) -> bool:
        """
        Indicate if language is testable

        :return: True if language is testable, False otherwise
        """

        return bool(self.container_info)


LANGUAGE_TEXT_TO_SYMBOL = {"plus": "+", "sharp": "#", "star": "*"}


def _get_language_display_name(language: str) -> str:
    tokens = [LANGUAGE_TEXT_TO_SYMBOL.get(token, token) for token in language.split("-")]
    separator = " "
    if any(token in LANGUAGE_TEXT_TO_SYMBOL.values() for token in tokens):
        separator = ""

    return separator.join(tokens).title()


__all__ = ["ContainerInfo", "FolderInfo", "TestInfo"]
