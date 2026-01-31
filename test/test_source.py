import os

import pytest

from glotter.core.source import CoreSource
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
TEST_INFO_NO_BUILD = TestInfo(
    container_info=CONTAINER_INFO_NO_BUILD, file_info=FOLDER_INFO_NO_BUILD
)

EXPECTED_CONTAINER_INFO_NO_BUILD = ContainerInfo(
    image=IMAGE_NO_BUILD, tag=TAG_NO_BUILD, cmd="python hello_world.py"
)
EXPECTED_TEST_INFO_NO_BUILD = TestInfo(
    container_info=EXPECTED_CONTAINER_INFO_NO_BUILD, file_info=FOLDER_INFO_NO_BUILD
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
TEST_INFO_BUILD = TestInfo(container_info=CONTAINER_INFO_BUILD, file_info=FOLDER_INFO_BUILD)

EXPECTED_CONTAINER_INFO_BUILD = ContainerInfo(
    image=IMAGE_BUILD,
    tag=TAG_BUILD,
    build="go build -o hello-world hello-world.go",
    cmd="./hello-world",
)
EXPECTED_TEST_INFO_BUILD = TestInfo(
    container_info=EXPECTED_CONTAINER_INFO_BUILD, file_info=FOLDER_INFO_BUILD
)


def test_full_path():
    src = CoreSource(
        filename="name.py",
        language="python",
        path=os.path.join("this", "is", "a", "path"),
        test_info=TEST_INFO_STRING_NO_BUILD,
    )
    expected = os.path.join("this", "is", "a", "path", "name.py")
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
        path=os.path.join("this", "is", "a", "path"),
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
