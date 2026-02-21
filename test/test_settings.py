import json
import shutil
from pathlib import Path
from typing import Any

import pytest
import yaml

from glotter_core.project import AcronymScheme, CoreProject
from glotter_core.settings import CoreSettings, CoreSettingsParser

TEST_DATA_DIR = Path("test/data").resolve()


def setup_settings_parser(tmp_dir: str, path: str, contents: str) -> CoreSettingsParser:
    (Path(tmp_dir) / path).mkdir(parents=True, exist_ok=True)
    (Path(tmp_dir) / path / ".glotter.yml").write_text(contents, encoding="utf-8")
    return CoreSettingsParser(str(tmp_dir))


def read_yaml_test_data(filename: str) -> dict[str, Any]:
    with (TEST_DATA_DIR / filename).open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def read_json_test_data(filename: str) -> dict[str, Any]:
    contents = (TEST_DATA_DIR / filename).read_text(encoding="utf-8")
    return json.loads(contents)


def test_settings_parser_when_glotter_yml_does_not_exist(tmp_dir: str, recwarn):
    settings_parser = CoreSettingsParser(tmp_dir)
    assert settings_parser.yml_path == tmp_dir
    assert settings_parser.project_root == tmp_dir
    assert settings_parser.yml == {}
    assert len(recwarn.list) == 1
    assert ".glotter.yml not found" in str(recwarn.pop(UserWarning).message)


@pytest.mark.parametrize("expected", ["", "this/is/a/few/levels/deeper"])
def test_settings_parser_when_good_glotter_yml_exists(expected: str, tmp_dir: str, recwarn):
    glotter_yml = (TEST_DATA_DIR / "good_glotter.yml").read_text(encoding="utf-8")
    settings_parser = setup_settings_parser(tmp_dir, expected, glotter_yml)

    expected_yml_path = Path(tmp_dir) / expected / ".glotter.yml"
    expected_yml = read_yaml_test_data("good_glotter.yml")

    assert settings_parser.yml_path == str(expected_yml_path)
    assert settings_parser.project_root == tmp_dir
    assert settings_parser.yml == expected_yml
    assert len(recwarn.list) == 0


def test_settings_parser_when_bad_glotter_yml_exists(tmp_dir: str):
    expected = ""
    glotter_yml = (TEST_DATA_DIR / "bad_glotter.yml").read_text(encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        setup_settings_parser(tmp_dir, expected, glotter_yml)

    assert ".glotter.yml does not contain a dict" in str(exc.value)


@pytest.mark.parametrize(
    ("filename_no_ext"),
    [
        pytest.param("empty_glotter", id="empty"),
        pytest.param("good_glotter", id="no-acronym-scheme-or-source-root"),
        pytest.param("good_glotter_with_source_and_acronyms", id="acronym-scheme-and-source-root"),
    ],
)
def test_settings_when_good_yml(filename_no_ext: str, tmp_dir_chdir: str):
    shutil.copy(TEST_DATA_DIR / f"{filename_no_ext}.yml", ".glotter.yml")

    settings = CoreSettings()

    expected_data = read_json_test_data(f"{filename_no_ext}.json")
    expected_settings = expected_data["settings"]
    expected_settings["acronym_scheme"] = AcronymScheme[expected_settings["acronym_scheme"]]
    assert settings.acronym_scheme == expected_settings["acronym_scheme"]
    assert settings.source_root == str(Path(tmp_dir_chdir) / expected_settings["source_root"])

    expected_project_items = expected_data["projects"]
    for project in expected_project_items.values():
        project["acronym_scheme"] = expected_settings["acronym_scheme"]

    expected_projects = {
        name: CoreProject(**project) for name, project in expected_project_items.items()
    }
    assert settings.projects == expected_projects


@pytest.mark.parametrize(
    ("filename", "expected_error"),
    [
        pytest.param(
            "bad_glotter_settings.yml", "settings does not contain a dict", id="bad-settings"
        ),
        pytest.param(
            "bad_glotter_acronym_scheme.yml",
            'Unknown acronym scheme: "bad"',
            id="bad-acronym-scheme",
        ),
        pytest.param(
            "bad_glotter_projects.yml", "projects does not contain a dict", id="bad-projects"
        ),
    ],
)
def test_settings_when_bad_yml(filename: str, expected_error: str, tmp_dir_chdir: str):
    shutil.copy(TEST_DATA_DIR / filename, ".glotter.yml")

    with pytest.raises(ValueError) as exc:
        CoreSettings()

    assert expected_error in str(exc.value)
