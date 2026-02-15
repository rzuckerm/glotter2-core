from pathlib import Path

import pytest
import yaml

from glotter.core.settings import CoreSettings
from glotter.core.source import CoreSource, CoreSourceCategories, categorize_sources
from glotter.core.testinfo import ContainerInfo, FolderInfo, TestInfo

EXTENSION_NO_BUILD = ".py"
NAMING_NO_BUILD = "underscore"
IMAGE_NO_BUILD = "python"
TAG_NO_BUILD = "3.7-alpine"
CMD_NO_BUILD = "python {{ source.name }}{{ source.extension }}"
TEST_INFO_STRING_NO_BUILD = f"""\
folder:
    extension: "{EXTENSION_NO_BUILD}"
    naming: "{NAMING_NO_BUILD}"

container:
    image: "{IMAGE_NO_BUILD}"
    tag: "{TAG_NO_BUILD}"
    cmd: "{CMD_NO_BUILD}"
"""
FOLDER_INFO_NO_BUILD = FolderInfo(extension=EXTENSION_NO_BUILD, naming=NAMING_NO_BUILD)
CONTAINER_INFO_NO_BUILD = ContainerInfo(image=IMAGE_NO_BUILD, tag=TAG_NO_BUILD, cmd=CMD_NO_BUILD)

EXPECTED_CONTAINER_INFO_NO_BUILD = ContainerInfo(
    image=IMAGE_NO_BUILD, tag=TAG_NO_BUILD, cmd="python hello_world.py"
)
EXPECTED_TEST_INFO_NO_BUILD = TestInfo(
    container_info=EXPECTED_CONTAINER_INFO_NO_BUILD,
    file_info=FOLDER_INFO_NO_BUILD,
    language_display_name="Python",
    notes=[],
)

EXTENSION_BUILD = ".go"
NAMING_BUILD = "hyphen"
IMAGE_BUILD = "golang"
TAG_BUILD = "1.12-alpine"
BUILD_BUILD = "go build -o {{ source.name }} {{ source.name}}{{ source.extension }}"
CMD_BUILD = "./{{ source.name }}"
TEST_INFO_STRING_BUILD = f"""\
folder:
    extension: "{EXTENSION_BUILD}"
    naming: "{NAMING_BUILD}"

container:
    image: "{IMAGE_BUILD}"
    tag: "{TAG_BUILD}"
    build: "{BUILD_BUILD}"
    cmd: "{CMD_BUILD}"
"""
FOLDER_INFO_BUILD = FolderInfo(extension=EXTENSION_BUILD, naming=NAMING_BUILD)
CONTAINER_INFO_BUILD = ContainerInfo(
    image=IMAGE_BUILD,
    tag=TAG_BUILD,
    build=BUILD_BUILD,
    cmd=CMD_BUILD,
)

EXPECTED_CONTAINER_INFO_BUILD = ContainerInfo(
    image=IMAGE_BUILD,
    tag=TAG_BUILD,
    build="go build -o hello-world hello-world.go",
    cmd="./hello-world",
)
EXPECTED_TEST_INFO_BUILD = TestInfo(
    container_info=EXPECTED_CONTAINER_INFO_BUILD,
    file_info=FOLDER_INFO_BUILD,
    language_display_name="Go",
    notes=[],
)


def test_full_path():
    src = CoreSource(
        filename="name.py",
        language="python",
        path=str(Path("this", "is", "a", "path")),
        test_info=TEST_INFO_STRING_NO_BUILD,
    )
    expected = str(Path("this", "is", "a", "path", "name.py"))
    actual = src.full_path
    assert actual == expected


@pytest.mark.parametrize(
    ("filename", "expected_name", "expected_extension"),
    [("name", "name", ""), ("name.ext", "name", ".ext"), ("name.ext1.ext2", "name", ".ext1.ext2")],
)
def test_basename_and_extension(filename, expected_name, expected_extension):
    src = CoreSource(
        filename=filename,
        language="python",
        path=str(Path("this", "is", "a", "path")),
        test_info=TEST_INFO_STRING_NO_BUILD,
    )
    assert src.name == expected_name
    assert src.extension == expected_extension


@pytest.mark.parametrize(
    ("filename", "language", "test_info_string", "expected_test_info"),
    [
        pytest.param(
            "hello_world.py",
            "python",
            TEST_INFO_STRING_NO_BUILD,
            EXPECTED_TEST_INFO_NO_BUILD,
            id="no-build",
        ),
        pytest.param(
            "hello-world.go", "go", TEST_INFO_STRING_BUILD, EXPECTED_TEST_INFO_BUILD, id="build"
        ),
    ],
)
def test_test_info_matches_test_info_string(
    filename, language, test_info_string, expected_test_info
):
    src = CoreSource(
        filename=filename, language=language, path="some-path", test_info=test_info_string
    )
    assert src.test_info == expected_test_info


def test_categorize_sources():
    settings = CoreSettings()
    categories = categorize_sources(settings.source_root, settings.projects, CoreSource)

    expected_categories = CoreSourceCategories()
    testable_languages = ["c-plus-plus", "python"]
    untestable_languages = ["mathematica"]
    languages = testable_languages + untestable_languages
    test_info_strs = {}
    paths = {}
    for language in languages:
        paths[language] = Path(settings.source_root, language[0], language)
        testinfo_path = paths[language] / "testinfo.yml"
        test_info_strs[language] = testinfo_path.read_text(encoding="utf-8")
        expected_categories.test_info[language] = TestInfo.from_dict(
            yaml.safe_load(test_info_strs[language]), language
        )

    expected_sources = {
        "c-plus-plus": {
            "helloworld": CoreSource(
                "hello-world.cpp",
                "c-plus-plus",
                str(paths["c-plus-plus"]),
                test_info_strs["c-plus-plus"],
            )
        },
        "mathematica": {
            "helloworld": CoreSource(
                "hello-world.nb",
                "mathematica",
                str(paths["mathematica"]),
                test_info_strs["mathematica"],
            )
        },
        "python": {
            "helloworld": CoreSource(
                "hello_world.py",
                "python",
                str(paths["python"]),
                test_info_strs["python"],
            ),
            "rot13": CoreSource(
                "rot13.py",
                "python",
                str(paths["python"]),
                test_info_strs["python"],
            ),
        },
    }
    expected_categories.by_language = {
        language: [source for source in project_sources.values()]
        for language, project_sources in expected_sources.items()
    }

    expected_categories.testable_by_project = {
        project_type: [] for project_type in settings.projects
    }
    for language, project_sources in expected_sources.items():
        if language in testable_languages:
            for project_type, source in project_sources.items():
                expected_categories.testable_by_project[project_type].append(source)

    expected_categories.bad_sources = [
        str(Path("m", "mathematica", "junk.nb")),
        str(Path("p", "python", "foo.py")),
    ]
    _assert_categorized_sources_eq(categories.by_language, expected_categories.by_language)
    _assert_categorized_sources_eq(
        categories.testable_by_project, expected_categories.testable_by_project
    )
    assert categories.test_info == expected_categories.test_info
    assert set(categories.bad_sources) == set(expected_categories.bad_sources)


def _assert_categorized_sources_eq(
    categorized_sources1: dict[str, list[CoreSource]],
    categorized_sources2: dict[str, list[CoreSource]],
) -> bool:
    assert set(categorized_sources1) == set(categorized_sources2)
    for key, sources in categorized_sources2.items():
        _assert_sources_eq(categorized_sources1[key], sources)


def _assert_sources_eq(sources1: CoreSource, sources2: CoreSource) -> bool:
    sources1 = sorted(sources1, key=lambda x: x.filename)
    sources2 = sorted(sources2, key=lambda x: x.filename)
    assert sources1 == sources2
