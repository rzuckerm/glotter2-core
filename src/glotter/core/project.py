"""Project information, acronym schemes, and naming schemes."""

from dataclasses import dataclass, field
from enum import Enum


class NamingScheme(Enum):
    """
    Naming scheme for project filename. This defines how the project words are
    converted to a filename.

    :ivar hyphen: all words are separated by a hyphen (e.g., ``hello-world``)
    :ivar underscore: all words are separated by underscore (e.g.,
        ``hello_world``)
    :ivar camel: the first word is lowercase, the remaining words are title case,
        and all words are joined together (e.g., ``helloWorld``)
    :ivar pascal: all words are title case and joined together (e.g.,
        ``HelloWorld``)
    :ivar lower: all words are lowercase and joined together (e.g.,
        ``helloworld``)
    """

    hyphen = "hyphen"
    underscore = "underscore"
    camel = "camel"
    pascal = "pascal"
    lower = "lower"


class AcronymScheme(Enum):
    """
    The acronym scheme overrides the naming scheme (:class:`NamingScheme`).
    Each project word is checked against a list of acronyms. If there is a
    match, then the acronym scheme applies.

    :ivar lower: acronym word is lowercase
    :ivar upper: acronym word is uppercase
    :ivar two_letter_limit: acronym word is uppercase if the naming scheme is
        ``camel`` or ``pascal``
    """

    lower = "lower"
    upper = "upper"
    two_letter_limit = "two_letter_limit"


@dataclass(frozen=True)
class CoreProject:
    """
    Project information

    :ivar words: Project words
    :ivar acronyms: Optional project acronyms. Default is no acronyms
    :ivar acronym_scheme: Optional project acronym scheme. Default is
        ``two_letter_limit``
    """

    words: list[str]
    acronyms: list[str] = field(default_factory=list)
    acronym_scheme: AcronymScheme = AcronymScheme.two_letter_limit

    def __post_init__(self):
        object.__setattr__(self, "acronyms", [acronym.upper() for acronym in self.acronyms])

    def get_project_name_by_scheme(self, naming: NamingScheme) -> str:
        """
        Get project name by on the specified naming scheme, the acronym scheme,
        the project words, and the project acronyms

        :param naming: Naming scheme
        :return: Project name
        :raises: :exc:`KeyError` if invalid naming scheme
        """

        try:
            return {
                NamingScheme.hyphen: self._as_hyphen,
                NamingScheme.underscore: self._as_underscore,
                NamingScheme.camel: self._as_camel,
                NamingScheme.pascal: self._as_pascal,
                NamingScheme.lower: self._as_lower,
            }[naming]()
        except KeyError as e:
            raise KeyError(f'Unknown naming scheme "{naming}"') from e

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


__all__ = ["AcronymScheme", "CoreProject", "NamingScheme"]
