from dataclasses import dataclass, field
from uuid import uuid4 as uuid

import pytest

from glotter.core.project import CoreProject
from glotter.core.testinfo import ContainerInfo, FolderInfo, TestInfo


@pytest.mark.parametrize("build", [uuid().hex, None], ids=["with_build", "without_build"])
def test_container_info_from_dict(build):
    dct = {
        "image": uuid().hex,
        "tag": uuid().hex,
        "cmd": uuid().hex,
    }
    expected = ContainerInfo(image=dct["image"], tag=dct["tag"], cmd=dct["cmd"], build=build)
    if build is not None:
        dct["build"] = build
    info = ContainerInfo.from_dict(dct)
    assert info == expected


def test_folder_info_from_dict():
    dct = {"extension": ".py", "naming": "underscore"}
    expected = FolderInfo(
        extension=dct["extension"],
        naming=dct["naming"],
    )
    info = FolderInfo.from_dict(dct)
    assert info == expected


def test_folder_info_bad_naming_scheme():
    dct = {"extension": ".py", "naming": "bad"}
    with pytest.raises(ValueError) as exc:
        FolderInfo.from_dict(dct)

    assert "Unknown naming scheme" in exc.value.args[0]


@pytest.mark.parametrize(
    "include_extension,expected_extension",
    [(True, ".py"), (False, "")],
    ids=["with_extension", "without_extension"],
)
def test_folder_info_get_project_mappings(include_extension, expected_extension):
    projects = {
        "helloworld": CoreProject(words=["hello", "world"]),
        "fibonacci": CoreProject(words=["fibonacci"]),
    }
    folder_info = FolderInfo(extension=".py", naming="underscore")

    project_mappings = folder_info.get_project_mappings(projects, include_extension)

    expected_project_mappings = {
        "helloworld": f"hello_world{expected_extension}",
        "fibonacci": f"fibonacci{expected_extension}",
    }
    assert project_mappings == expected_project_mappings


@dataclass
class ExpectedTestInfo:
    folder_info_dict: dict[str, str]
    language: str
    expected_language_display_name: str
    build: str = ""
    language_display_name: str = ""
    notes: list = field(default_factory=list)
    has_container_info: bool = True


@pytest.mark.parametrize(
    "expected_test_info",
    [
        pytest.param(
            ExpectedTestInfo(
                folder_info_dict={"extension": ".py", "naming": "underscore"},
                language="python",
                expected_language_display_name="Python",
            ),
            id="defaults",
        ),
        pytest.param(
            ExpectedTestInfo(
                folder_info_dict={"extension": ".php", "naming": "hyphen"},
                language="php",
                language_display_name="PHP",
                expected_language_display_name="PHP",
            ),
            id="has-language-display-name",
        ),
        pytest.param(
            ExpectedTestInfo(
                folder_info_dict={"extension": ".cpp", "naming": "hyphen"},
                build="cpp -o {{ source.name }} {{ source.name }}{{ source.extension }}",
                language="c-plus-plus",
                expected_language_display_name="C++",
            ),
            id="language-with-plus",
        ),
        pytest.param(
            ExpectedTestInfo(
                folder_info_dict={"extension": ".cs", "naming": "hyphen"},
                language="c-sharp",
                expected_language_display_name="C#",
            ),
            id="language-with-sharp",
        ),
        pytest.param(
            ExpectedTestInfo(
                folder_info_dict={"extension": ".cx", "naming": "hyphen"},
                language="c-star",
                expected_language_display_name="C*",
            ),
            id="language-with-star",
        ),
        pytest.param(
            ExpectedTestInfo(
                folder_info_dict={"extension": ".m4", "naming": "hyphen"},
                language="m4",
                language_display_name="m4",
                expected_language_display_name="m4",
                notes=[
                    "Parameters are automatically enclosed in backtick (`) and single quote (')"
                ],
            ),
            id="has-language-display-name-and-notes",
        ),
        pytest.param(
            ExpectedTestInfo(
                folder_info_dict={"extension": ".m4", "naming": "hyphen"},
                language="m4",
                language_display_name="m4",
                expected_language_display_name="m4",
                notes=[
                    "Parameters are automatically enclosed in backtick (`) and single quote (')"
                ],
            ),
            id="has-language-display-name-and-notes",
        ),
        pytest.param(
            ExpectedTestInfo(
                folder_info_dict={"extension": ".m", "naming": "hyphen"},
                language="objective-c",
                expected_language_display_name="Objective C",
            ),
            id="multi-word-language",
        ),
        pytest.param(
            ExpectedTestInfo(
                folder_info_dict={"extension": ".nb", "naming": "hyphen"},
                language="mathematica",
                expected_language_display_name="Mathematica",
                has_container_info=False,
                notes=["Mathematica requires a commercial license, so it cannot be tested"],
            ),
            id="has-notes-and-no-container",
        ),
    ],
)
def test_test_info_from_dict(expected_test_info):
    container_info_dict = _get_container_info_dict(
        expected_test_info.has_container_info, expected_test_info.build
    )
    ci = ContainerInfo(**container_info_dict)
    fi = FolderInfo(**expected_test_info.folder_info_dict)
    test_info_dict = {
        "container": container_info_dict,
        "folder": expected_test_info.folder_info_dict,
    }
    if expected_test_info.language_display_name:
        test_info_dict["language_display_name"] = expected_test_info.language_display_name

    if expected_test_info.notes:
        test_info_dict["notes"] = expected_test_info.notes

    test_info = TestInfo.from_dict(test_info_dict, language=expected_test_info.language)
    expected = TestInfo(
        container_info=ci,
        file_info=fi,
        language_display_name=expected_test_info.expected_language_display_name,
        notes=expected_test_info.notes,
    )
    assert test_info == expected


@pytest.mark.parametrize("is_testable", [True, False])
def test_test_info_is_testable(is_testable):
    container_info_dict = _get_container_info_dict(is_testable)
    folder_info_dict = {"extension": ".foo", "naming": "hyphen"}
    test_info_dict = {
        "container": container_info_dict,
        "folder": folder_info_dict,
    }
    test_info = TestInfo.from_dict(test_info_dict, language="foo")

    assert test_info.is_testable is is_testable


def _get_container_info_dict(is_testable, build=""):
    container_info_dict = {}
    if is_testable:
        container_info_dict = {
            "image": uuid().hex,
            "tag": uuid().hex,
            "cmd": uuid().hex,
        }
        if build:
            container_info_dict["build"] = build

    return container_info_dict
