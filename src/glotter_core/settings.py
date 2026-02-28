"""Project settings"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from warnings import warn

import yaml

from .project import AcronymScheme, CoreProject


@dataclass(frozen=True, init=False)
class CoreSettings:
    """Global project settings

    :raises: :exc:`ValueError` if invalid settings

    :ivar str project_root: Root directory of project
    :ivar src source_root: Root directory for source files
    :ivar AcronymScheme acronym_scheme: Optional project acronym scheme.
        Default is :const:`AcronymScheme.two_letter_limit`
    :ivar projects: Dictionary whose key is the project name and whose value
        is the project information
    """

    project_root: str = ""
    acronym_scheme: AcronymScheme = AcronymScheme.two_letter_limit
    source_root: str = ""
    projects: dict[str | CoreProject] = field(default=dict)

    def __init__(self) -> None:
        object.__setattr__(self, "project_root", str(Path.cwd()))
        parser = CoreSettingsParser(self.project_root)
        self._set_global_settings(parser.yml.get("settings", {}))
        self._set_projects(parser.yml.get("projects", {}))

    def _set_global_settings(self, settings_item: Any) -> None:
        if not isinstance(settings_item, dict):
            raise ValueError("settings does not contain a dict")

        acronym_scheme = settings_item.get("acronym_scheme", "two_letter_limit")
        try:
            object.__setattr__(self, "acronym_scheme", AcronymScheme[acronym_scheme])
        except KeyError:
            raise ValueError(f'Unknown acronym scheme: "{acronym_scheme}"')

        source_root = settings_item.get("source_root") or self.project_root
        object.__setattr__(self, "source_root", str(Path(source_root).resolve()))

    def _set_projects(self, projects_item: dict[str, Any]) -> None:
        if not isinstance(projects_item, dict):
            raise ValueError("projects does not contain a dict")

        projects = {name: CoreProject(project) for name, project in projects_item.items()}
        object.__setattr__(self, "projects", projects)


@dataclass(frozen=True, init=False)
class CoreSettingsParser:
    """Parse the settings file (``.glotter.yml``)

    :param project_root: Root directory of project
    :raises: :exc:`ValueError` if setting file does not contain a dictionary

    :ivar str project_root: Root directory of project
    :ivar str | None yml_path: Path to ``.glotter.yml`` file
    :ivar dict[str, Any] yml: Contents of ``.glotter.yml`` file
    """

    project_root: str
    yml_path: str | None = None
    yml: dict[str, Any] = field(default_factory=dict, repr=False)

    def __init__(self, project_root):
        object.__setattr__(self, "project_root", project_root)
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
                return str((Path(root) / ".glotter.yml").resolve())

        return None


__all__ = ["CoreSettings", "CoreSettingsParser"]
