"""Project settings"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from warnings import warn

import yaml


@dataclass(frozen=True)
class CoreSettingsParser:
    """Parse the setting file (``.glotter.yml``)

    :param project_root: Root directory of project
    :raises: :exc:`ValueError` if setting file does not contain a dictionary

    :ivar project_root: Root directory of project
    :ivar yml_path: Path to ``.glotter.yml`` file
    :ivar yml: Contents of ``.glotter.yml`` file
    """

    project_root: str
    yml_path: str | None = None
    yml: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, "yml_path", self._locate_yml())

        yml = None
        if self.yml_path is not None:
            yml = self._parse_yml()
        else:
            object.__setattr__(self, "yml_path", self.project_root)
            warn(f'.glotter.yml not found in directory "{self.project_root}"')

        if yml is None:
            yml = {}

        if not isinstance(yml, dict):
            raise ValueError(".glotter.yml does not contain a dict")

        object.__setattr__(self, "yml", yml)

    def _parse_yml(self) -> Any:
        contents = Path(self.yml_path).read_text(encoding="utf-8")
        return yaml.safe_load(contents)

    def _locate_yml(self) -> str | None:
        for root, _, files in os.walk(self.project_root):
            if ".glotter.yml" in files:
                return str((Path(root) / ".glotter.yml").absolute())

        return None


__all__ = ["CoreSettingsParser"]
