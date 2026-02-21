"""Source information"""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from glotter_core.project import CoreProjectMixin
from glotter_core.testinfo import TestInfo


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


@dataclass
class CoreSourceCategories:
    """
    Categories for sources

    :ivar testable_by_project: dictionary whose key is the project type and
        whose value is a testable source object
    :ivar by_language: dictionary whose key is the language and whose
        value is a source object
    :ivar test_info: dictionary whose key is the language name and whose value
        is a TestInfo object
    :ivar bad_sources: list of filenames that do not belong to a project
    """

    testable_by_project: dict[str, CoreSource] = field(default_factory=dict)
    by_language: dict[str, CoreSource] = field(default_factory=dict)
    test_info: dict[str, TestInfo] = field(default_factory=dict)
    bad_sources: list[str] = field(default_factory=list)


_IGNORED_FILENAMES = {"untestable.yml", "testinfo.yml", "README.md"}


def categorize_sources(
    path: str, projects: dict[str, CoreProjectMixin], source_cls: type
) -> CoreSourceCategories:
    """
    Categorize sources

    :param path: path to source directory
    :param projects: dictionary whose key is a project type and whose value is a
        CoreProjectMixin object
    :param source_cls: source object class
    :return: CoreSourceCategories object containing information of the source
        categories
    """

    categories = CoreSourceCategories()
    categories.testable_by_project = {k: [] for k in projects}
    orig_path = Path(path).resolve()
    for root, _, files in os.walk(path):
        current_path = Path(root).resolve()
        if "testinfo.yml" in files:
            test_info_string = Path(current_path, "testinfo.yml").read_text(encoding="utf-8")
            language = current_path.name
            test_info = TestInfo.from_dict(yaml.safe_load(test_info_string), language)
            categories.test_info[language] = test_info
            folder_info = test_info.file_info
            folder_project_names = folder_info.get_project_mappings(
                projects, include_extension=True
            )
            for project_type, project_name in folder_project_names.items():
                if project_name in files:
                    source = source_cls(project_name, language, str(current_path), test_info_string)
                    categories.by_language.setdefault(language, []).append(source)
                    if source.test_info.is_testable:
                        categories.testable_by_project[project_type].append(source)

            invalid_filenames = set(files) - (
                set(folder_project_names.values()) | _IGNORED_FILENAMES
            )
            categories.bad_sources += [
                str(current_path.relative_to(orig_path) / filename)
                for filename in invalid_filenames
            ]

    return categories


__all__ = ["CoreSource", "CoreSourceCategories", "categorize_sources"]
