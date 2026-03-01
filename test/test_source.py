import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import pytest
import yaml

from glotter_core.settings import CoreSettings
from glotter_core.source import CoreLanguage, CoreSource, CoreSourceCategories, categorize_sources
from glotter_core.testinfo import ContainerInfo, FolderInfo, TestInfo

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
        project_type="someproject",
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
        project_type="someproject",
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
        filename=filename,
        language=language,
        path="some-path",
        test_info=test_info_string,
        project_type="someproject",
    )
    assert src.test_info == expected_test_info


def test_categorize_sources():
    with cd("test/data/sample-programs-repo"):
        settings = CoreSettings()

    categories = categorize_sources(settings.source_root, settings.projects, CoreSource)

    expected_categories = CoreSourceCategories()
    testable_languages = ["c-plus-plus", "python"]
    untestable_languages = ["mathematica"]
    languages = testable_languages + untestable_languages
    test_info_strs = {}
    test_info_paths = {}
    test_infos = {}
    paths = {}
    for language in languages:
        paths[language] = Path(settings.source_root, language[0], language)
        test_info_paths[language] = paths[language] / "testinfo.yml"
        test_info_strs[language] = test_info_paths[language].read_text(encoding="utf-8")
        test_infos[language] = TestInfo.from_dict(
            yaml.safe_load(test_info_strs[language]), language
        )

    expected_sources = {
        "c-plus-plus": {
            "helloworld": CoreSource(
                filename="hello-world.cpp",
                language="c-plus-plus",
                path=str(paths["c-plus-plus"]),
                test_info=test_info_strs["c-plus-plus"],
                project_type="helloworld",
            )
        },
        "mathematica": {
            "helloworld": CoreSource(
                filename="hello-world.nb",
                language="mathematica",
                path=str(paths["mathematica"]),
                test_info=test_info_strs["mathematica"],
                project_type="helloworld",
            )
        },
        "python": {
            "helloworld": CoreSource(
                filename="hello_world.py",
                language="python",
                path=str(paths["python"]),
                test_info=test_info_strs["python"],
                project_type="helloworld",
            ),
            "rot13": CoreSource(
                filename="rot13.py",
                language="python",
                path=str(paths["python"]),
                test_info=test_info_strs["python"],
                project_type="rot13",
            ),
        },
    }
    expected_categories.by_language = {
        language: CoreLanguage(
            sources=[source for source in project_sources.values()],
            test_info=test_infos[language],
            test_info_path=test_info_paths[language],
        )
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
    _assert_categorized_languages_eq(categories.by_language, expected_categories.by_language)
    _assert_categorized_sources_eq(
        categories.testable_by_project, expected_categories.testable_by_project
    )
    assert set(categories.bad_sources) == set(expected_categories.bad_sources)


def test_categorize_sources_untestable():
    with cd("test/data/untestable"):
        settings = CoreSettings()

    categories = categorize_sources(settings.source_root, settings.projects, CoreSource)

    expected_categories = CoreSourceCategories()
    untestable_info = {
        "untestable-camel": {"extension": ".uc", "naming": "camel"},
        "untestable-hyphen": {"extension": ".uh", "naming": "hyphen"},
        "untestable-lower": {"extension": ".ul", "naming": "lower"},
        "untestable-pascal": {"extension": ".up", "naming": "pascal"},
        "untestable-underscore": {"extension": ".uu", "naming": "underscore"},
    }
    test_info_strs = {}
    test_info_paths = {}
    test_infos = {}
    paths = {}
    for language, folder_info in untestable_info.items():
        paths[language] = Path(settings.source_root, language[0], language)
        test_info_paths[language] = paths[language] / "untestable.yml"
        untestable = yaml.safe_load(test_info_paths[language].read_text(encoding="utf-8"))
        test_info_dict = {"folder": folder_info, "notes": [untestable[0]["reason"]]}
        test_info_strs[language] = yaml.safe_dump(test_info_dict)
        test_infos[language] = TestInfo.from_dict(test_info_dict, language)

    expected_categories.testable_by_project = {
        project_type: [] for project_type in settings.projects
    }

    expected_sources = {
        "untestable-camel": {
            "helloworld": CoreSource(
                filename="helloWorld.uc",
                language="untestable-camel",
                path=str(paths["untestable-camel"]),
                test_info=test_info_strs["untestable-camel"],
                project_type="helloworld",
            ),
            "rot13": CoreSource(
                filename="rot13.uc",
                language="untestable-camel",
                path=str(paths["untestable-camel"]),
                test_info=test_info_strs["untestable-camel"],
                project_type="rot13",
            ),
        },
        "untestable-hyphen": {
            "helloworld": CoreSource(
                filename="hello-world.uh",
                language="untestable-hyphen",
                path=str(paths["untestable-hyphen"]),
                test_info=test_info_strs["untestable-hyphen"],
                project_type="helloworld",
            ),
            "rot13": CoreSource(
                filename="rot13.uh",
                language="untestable-hyphen",
                path=str(paths["untestable-hyphen"]),
                test_info=test_info_strs["untestable-hyphen"],
                project_type="rot13",
            ),
        },
        "untestable-lower": {
            "helloworld": CoreSource(
                filename="helloworld.ul",
                language="untestable-lower",
                path=str(paths["untestable-lower"]),
                test_info=test_info_strs["untestable-lower"],
                project_type="helloworld",
            ),
            "rot13": CoreSource(
                filename="rot13.ul",
                language="untestable-lower",
                path=str(paths["untestable-lower"]),
                test_info=test_info_strs["untestable-lower"],
                project_type="rot13",
            ),
        },
        "untestable-pascal": {
            "helloworld": CoreSource(
                filename="HelloWorld.up",
                language="untestable-pascal",
                path=str(paths["untestable-pascal"]),
                test_info=test_info_strs["untestable-pascal"],
                project_type="helloworld",
            ),
            "rot13": CoreSource(
                filename="Rot13.up",
                language="untestable-pascal",
                path=str(paths["untestable-pascal"]),
                test_info=test_info_strs["untestable-pascal"],
                project_type="rot13",
            ),
        },
        "untestable-underscore": {
            "helloworld": CoreSource(
                filename="hello_world.uu",
                language="untestable-underscore",
                path=str(paths["untestable-underscore"]),
                test_info=test_info_strs["untestable-underscore"],
                project_type="helloworld",
            ),
            "rot13": CoreSource(
                filename="rot13.uu",
                language="untestable-underscore",
                path=str(paths["untestable-underscore"]),
                test_info=test_info_strs["untestable-underscore"],
                project_type="rot13",
            ),
        },
    }
    expected_categories.by_language = {
        language: CoreLanguage(
            sources=[source for source in project_sources.values()],
            test_info=test_infos[language],
            test_info_path=test_info_paths[language],
        )
        for language, project_sources in expected_sources.items()
    }
    _assert_categorized_languages_eq(categories.by_language, expected_categories.by_language)
    _assert_categorized_sources_eq(
        categories.testable_by_project, expected_categories.testable_by_project
    )
    assert set(categories.bad_sources) == set(expected_categories.bad_sources)


def _assert_categorized_languages_eq(
    languages1: dict[str, CoreLanguage], languages2: dict[str, CoreLanguage]
) -> None:
    assert set(languages1) == set(languages2)
    for language, language_info2 in languages2.items():
        language_info1 = languages1[language]
        _assert_sources_eq(language_info1.sources, language_info2.sources)
        assert language_info1.test_info == language_info2.test_info
        assert language_info1.test_info_path == language_info2.test_info_path


def _assert_categorized_sources_eq(
    categorized_sources1: dict[str, list[CoreSource]],
    categorized_sources2: dict[str, list[CoreSource]],
) -> None:
    assert set(categorized_sources1) == set(categorized_sources2)
    for key, sources in categorized_sources2.items():
        _assert_sources_eq(categorized_sources1[key], sources)


def _assert_sources_eq(sources1: list[CoreSource], sources2: list[CoreSource]) -> None:
    sources1 = sorted(sources1, key=lambda x: x.filename)
    sources2 = sorted(sources2, key=lambda x: x.filename)
    assert sources1 == sources2


@contextmanager
def cd(path: str) -> Generator[None, None, None]:
    orig_cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(orig_cwd)
