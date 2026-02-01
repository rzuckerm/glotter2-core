"""A collection of constant values and classes"""

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


__all__ = ["AcronymScheme", "NamingScheme"]
