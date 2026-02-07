from pathlib import Path

import pytest
import yaml

from glotter.core.settings import CoreSettingsParser

TEST_DATA_DIR = Path("test/data").absolute()


def setup_settings_parser(tmp_dir: str, path: str, contents: str) -> CoreSettingsParser:
    (Path(tmp_dir) / path).mkdir(parents=True, exist_ok=True)
    (Path(tmp_dir) / path / ".glotter.yml").write_text(contents, encoding="utf-8")
    return CoreSettingsParser(str(tmp_dir))


def test_settings_parser_when_glotter_yml_does_not_exist(tmp_dir: Path, recwarn):
    settings_parser = CoreSettingsParser(tmp_dir)
    assert settings_parser.yml_path == tmp_dir
    assert settings_parser.project_root == tmp_dir
    assert settings_parser.yml == {}
    assert len(recwarn.list) == 1
    assert ".glotter.yml not found" in str(recwarn.pop(UserWarning).message)


@pytest.mark.parametrize("expected", ["", "this/is/a/few/levels/deeper"])
def test_settings_parser_when_good_glotter_yml_exists(expected, tmp_dir, recwarn):
    glotter_yml = (TEST_DATA_DIR / "good_glotter.yml").read_text(encoding="utf-8")
    settings_parser = setup_settings_parser(tmp_dir, expected, glotter_yml)

    expected_yml_path = Path(tmp_dir) / expected / ".glotter.yml"
    with expected_yml_path.open(encoding="utf-8") as f:
        expected_yml = yaml.safe_load(f)

    assert settings_parser.yml_path == str(expected_yml_path)
    assert settings_parser.project_root == tmp_dir
    assert settings_parser.yml == expected_yml
    assert len(recwarn.list) == 0


def test_settings_parser_when_bad_glotter_yml_exists(tmp_dir):
    expected = ""
    glotter_yml = (TEST_DATA_DIR / "bad_glotter.yml").read_text(encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        setup_settings_parser(tmp_dir, expected, glotter_yml)

    assert ".glotter.yml does not contain a dict" in str(exc.value)
