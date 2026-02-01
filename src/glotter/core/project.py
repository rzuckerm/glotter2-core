"""Project information, acronym schemes, and naming schemes."""

from dataclasses import dataclass, field
from typing import Union

from .constants import AcronymScheme, NamingScheme


@dataclass(frozen=True)
class CoreProject:
    """
    Project information

    :param words: Project words
    :param acronyms: Optional project acronyms. Default is no acronyms
    :param acronym_scheme: Optional project acronym scheme. Default is
        ``two_letter_limit``
    :raises: :exc:`ValueError` if invalid acronym scheme

    :ivar words: Project words
    :ivar acronyms: Optional project acronyms. Default is no acronyms
    :ivar acronym_scheme: Optional project acronym scheme. Default is
        ``two_letter_limit``
    """

    words: list[str]
    acronyms: list[str] = field(default_factory=list)
    acronym_scheme: Union[str, AcronymScheme] = AcronymScheme.two_letter_limit

    def __post_init__(self):
        object.__setattr__(self, "acronyms", [acronym.upper() for acronym in self.acronyms])
        if not isinstance(self.acronym_scheme, AcronymScheme):
            try:
                object.__setattr__(self, "acronym_scheme", AcronymScheme[self.acronym_scheme])
            except KeyError as e:
                raise ValueError(f'Unknown acronym scheme: "{self.acronym_scheme}"') from e

    def get_project_name_by_scheme(self, naming: Union[str, NamingScheme]) -> str:
        """
        Get project name by on the specified naming scheme, the acronym scheme,
        the project words, and the project acronyms

        :param naming: Naming scheme
        :return: Project name
        :raises: :exc:`Value` if invalid naming scheme
        """

        try:
            if not isinstance(naming, NamingScheme):
                naming = NamingScheme[naming]

            return {
                NamingScheme.hyphen: self._as_hyphen,
                NamingScheme.underscore: self._as_underscore,
                NamingScheme.camel: self._as_camel,
                NamingScheme.pascal: self._as_pascal,
                NamingScheme.lower: self._as_lower,
            }[naming]()
        except KeyError as e:
            raise ValueError(f'Unknown naming scheme "{naming}"') from e

    @property
    def display_name(self) -> str:
        """
        Get display name for the project. The project words are separated by
        an spaces, subject to the acronym scheme -- e.g., ``hello world``).

        :return: Display name
        """

        return self._as_display()

    def _as_hyphen(self):
        return "-".join(self._try_as_acronym(word, NamingScheme.hyphen) for word in self.words)

    def _as_underscore(self):
        return "_".join(self._try_as_acronym(word, NamingScheme.underscore) for word in self.words)

    def _as_camel(self):
        return self.words[0].lower() + "".join(
            self._try_as_acronym(word.title(), NamingScheme.camel) for word in self.words[1:]
        )

    def _as_pascal(self):
        return "".join(
            self._try_as_acronym(word.title(), NamingScheme.pascal) for word in self.words
        )

    def _as_lower(self):
        return "".join(word.lower() for word in self.words)

    def _as_display(self):
        return " ".join(
            self._try_as_acronym(word.title(), NamingScheme.underscore) for word in self.words
        )

    def _is_acronym(self, word):
        return word.upper() in self.acronyms

    def _try_as_acronym(self, word, naming_scheme):
        if self._is_acronym(word):
            if self.acronym_scheme == AcronymScheme.upper:
                return word.upper()
            elif self.acronym_scheme == AcronymScheme.lower:
                return word.lower()
            elif len(word) <= 2 and naming_scheme in [
                NamingScheme.camel,
                NamingScheme.pascal,
            ]:
                return word.upper()

        return word


__all__ = ["CoreProject"]
