"""Source information"""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from glotter.core.project import CoreProjectMixin
from glotter.core.testinfo import FolderInfo, TestInfo

BAD_SOURCES = "__bad_sources__"


@dataclass(frozen=True)
class CoreSource:
    """Metadata about a source file

    :param filename: filename including extension
    :param language: the language of the source
    :param path: path to the file excluding name
    :param str test_info: a string in yaml format containing testinfo for a directory

    :ivar filename: filename including extension
    :ivar language: the language of the source
    :ivar path: path to the file excluding name
    :ivar TestInfo test_info: TestInfo object
    """

    filename: str
    language: str
    path: str
    test_info: str = field(repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "test_info", TestInfo.from_string(self.test_info, self))

    @property
    def full_path(self) -> str:
        """Returns the full path to the source including filename and extension"""
        return str(Path(self.path) / self.filename)

    @property
    def name(self) -> str:
        """Returns the name of the source excluding the extension"""
        return self.filename.split(".")[0]

    @property
    def extension(self) -> str:
        """Returns the extension of the source"""
        return "".join(Path(self.filename).suffixes)


def get_sources_by_project(
    path: str,
    projects: dict[str, CoreProjectMixin],
    source_cls: type,
    check_bad_sources: bool = False,
) -> dict[str, list]:
    """
    Walk through a directory and create source class objects for each project

    :param path: path to the directory through which to walk
    :param projects: dictionary whose key is the name of the project and whose value
        is a project object
    :param source_cls: class to use to create source
    :param check_bad_source: if True, check for bad source filenames. Default is False
    :return: a dict where the key is the project type and the value is a list of all the
        source objects of that project. If check_bad_source is True, the BAD_SOURCES
        key contains a list of invalid paths relative to the specified path
    """
    sources = {k: [] for k in projects}
    if check_bad_sources:
        sources[BAD_SOURCES] = []

    for root, _, files in os.walk(path):
        current_path = Path(root).resolve()
        if "testinfo.yml" in files:
            test_info_string = (current_path / "testinfo.yml").read_text(encoding="utf-8")
            folder_info = FolderInfo.from_dict(yaml.safe_load(test_info_string)["folder"])
            folder_project_names = folder_info.get_project_mappings(include_extension=True)
            for project_type, project_name in folder_project_names.items():
                if project_name in files:
                    source = source_cls(
                        project_name, current_path.name, str(current_path), test_info_string
                    )
                    sources[project_type].append(source)

            if check_bad_sources:
                invalid_filenames = set(files) - (
                    set(folder_project_names.values()) | {"testinfo.yml", "README.md"}
                )
                sources[BAD_SOURCES] += [
                    str(Path(path).relative_to(current_path) / filename)
                    for filename in invalid_filenames
                ]

    return sources


__all__ = ["BAD_SOURCES", "CoreSource", "get_sources_by_project"]
