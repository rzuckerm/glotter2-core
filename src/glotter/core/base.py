"""Abstraction classes"""

from typing import Protocol, Union

from .constants import NamingScheme


class BaseProject(Protocol):
    """Base class for an object that provides project information"""

    def get_project_name_by_scheme(self, naming: Union[str, NamingScheme]) -> str:
        """Get project name base on naming scheme"""
        ...


__all__ = ["BaseProject"]
